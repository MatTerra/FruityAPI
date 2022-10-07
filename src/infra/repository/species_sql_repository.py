from typing import Type

from nova_api.dao.generic_sql_dao import GenericSQLDAO
from nova_api.persistence import PersistenceHelper
from nova_api.persistence.postgresql_helper import PostgreSQLHelper

from core.entity.species import Species
from core.repository.species_repository import SpeciesRepository


class SpeciesSQLRepository(SpeciesRepository):
    def __init__(self):
        self.dao = SpeciesSQLDAO()

    def create(self, entity: Species):
        self.dao.create(entity)

    def update(self, entity: Species):
        self.dao.update(entity)

    def findOne(self, filters: dict):
        self.dao.get_all(1, 0, filters)

    def find(self, length=20, offset=0, filters: dict = None):
        if "popular_name" in filters:
            value = filters["popular_name"]
            del filters["popular_name"]
            filters["popular_names"] = ["@>", '{"'+value+'"}']
        self.dao.get_all(filters=filters)

    def findById(self, _id: str):
        self.dao.get(_id)

    def delete(self, _id: str):
        self.dao.remove(filters={"_id": _id})


class SpeciesSQLDAO(GenericSQLDAO):
    table = 'species'

    def __init__(self,
                 database_type: Type[PersistenceHelper] = PostgreSQLHelper,
                 **kwargs):
        super(SpeciesSQLDAO, self).__init__(
            database_type=database_type,
            table=SpeciesSQLDAO.table,
            return_class=Species,
            **kwargs
        )
        self.database.ALLOWED_COMPARATORS.append('@>')
