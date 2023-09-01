from typing import Type

from nova_api.dao.generic_sql_dao import GenericSQLDAO
from nova_api.persistence import PersistenceHelper
from nova_api.persistence.postgresql_helper import PostgreSQLHelper

from core.entity.tree import Tree
from core.repository.tree_repository import TreeRepository
from infra.repository.species_sql_repository import SpeciesSQLDAO, SpeciesSQLRepository


class TreeSQLRepository(TreeRepository):
    def __init__(self, dao=None):
        self.dao = dao or TreeSQLDAO()
        self.species_repository = SpeciesSQLRepository(SpeciesSQLDAO(database_instance=self.dao.database))

    def create(self, entity: Tree):
        return self.dao.create(entity)

    def update(self, entity: Tree):
        return self.dao.update(entity)

    def findOne(self, filters: dict):
        try:
            return self.find(filters=filters, length=1, offset=0)[1][0]
        except IndexError:
            return None

    def find(self, length=20, offset=0, filters=None, include_species=True):
        filters = filters if filters else {}
        near = None

        if "near" in filters:
            near = filters["near"]
            del filters["near"]

        if near is None:
            filters, query_params = self.dao._generate_filters(filters=filters) if filters else ('', [])
        else:
            filters, query_params = self.dao._generate_filters(
                filters=filters)
            filters += \
                f" ST_DWithin({self.dao.fields['location']}::geography, ST_GeogFromText('POINT(%s %s)'),%s, false)"
            query_params.extend(near)

        total, return_list = self.dao.get_all_by_custom_query(filters, query_params, length, offset)
        species_set = set([tree.species.id_ for tree in return_list])

        if len(return_list) > 0 and include_species:
            species = {specie.id_: specie for specie in self.species_repository.find(
                filters={"id_": ["IN", str(tuple(species_set))]}, length=len(species_set), offset=0
            )[1]}

            for tree in return_list:
                tree.species = species[tree.species.id_]

        return total, return_list

    def findById(self, _id: str):
        try:
            return self.find(length=1, offset=0, filters={"id_": _id})[1][0]
        except IndexError:
            return None

    def delete(self, _id: str):
        return self.dao.remove(filters={"id_": _id})


class TreeSQLDAO(GenericSQLDAO):
    table = 'Tree'

    def __init__(self,
                 database_type: Type[PersistenceHelper] = PostgreSQLHelper,
                 **kwargs):
        super(TreeSQLDAO, self).__init__(
            database_type=database_type,
            table=TreeSQLDAO.table,
            return_class=Tree,
            **kwargs
        )

    def create_table_if_not_exists(self) -> None:
        super().create_table_if_not_exists()
        self.database.query(f"CREATE INDEX ON tree USING GIST({self.fields['location']})")
        self.database.query(
            f"ALTER TABLE tree "
            f"ADD CONSTRAINT tree_species "
            f"FOREIGN KEY ({self.fields['species']}) "
            f"REFERENCES species (species_id_);"
        )

    def get_all_by_custom_query(self, filters, params, length=20, offset=0):
        query = self.database.SELECT_QUERY.format(
            fields=', '.join(self.fields.values()).replace('tree_location',
                                                           'ST_AsGeoJSON(tree_location) as tree_location'),
            table=self.table,
            filters=filters
        )

        self.database.query(query, [*params, length, offset])
        results = self.database.get_results()

        if results is None:
            return 0, []

        return_list = [self.return_class(*result) for result in results]

        query_total = self.database.QUERY_TOTAL_COLUMN.format(
            table=self.table,
            column=self.fields['id_'])

        self.database.query(query_total)
        total = self.database.get_results()[0][0]

        return total, return_list
