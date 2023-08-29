import datetime
from typing import Type

from nova_api.dao.generic_sql_dao import GenericSQLDAO
from nova_api.persistence import PersistenceHelper
from nova_api.persistence.postgresql_helper import PostgreSQLHelper

from core.entity.tree import Tree
from core.repository.tree_repository import TreeRepository


class TreeSQLRepository(TreeRepository):
    def __init__(self, dao=None):
        self.dao = TreeSQLDAO() if dao is None else dao

    def create(self, entity: Tree):
        return self.dao.create(entity)

    def update(self, entity: Tree):
        return self.dao.update(entity)

    def findOne(self, filters: dict):
        try:
            return self.find(filters=filters, length=1, offset=0)[1][0]
        except IndexError:
            return None

    def find(self, length=20, offset=0, filters=None):
        filters = filters if filters else {}
        near = None
        if "near" in filters:
            near = filters["near"]
            del filters["near"]
        if near is None:
            filters, query_params = self.dao._generate_filters(filters=filters) if filters else ('', [])
            return self.dao.get_all_by_custom_query(filters, query_params, 1, 0)
        else:
            filters_, query_params = self.dao._generate_filters(
                filters=filters)
            filters_ += \
                f" ST_DWithin({self.dao.fields['location']}::geography, ST_GeogFromText('POINT(%s %s)'),10000, false)"
            query_params.extend(near)
            return self.dao.get_all_by_custom_query(filters_, query_params,
                                                    length, offset)

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
        self.database.ALLOWED_COMPARATORS.append('<->')

    def create_table_if_not_exists(self) -> None:
        super().create_table_if_not_exists()
        self.database.query(f"CREATE INDEX ON tree USING GIST({self.fields['location']})")

    def get_all_by_custom_query(self, filters, params, length=20, offset=0):

        query = self.database.SELECT_QUERY.format(
            fields=', '.join(self.fields.values()).replace('tree_location', 'ST_AsGeoJSON(tree_location) as tree_location'),
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
