import datetime
from typing import Type

from nova_api.dao.generic_sql_dao import GenericSQLDAO
from nova_api.persistence import PersistenceHelper
from nova_api.persistence.postgresql_helper import PostgreSQLHelper

from core.entity.species import Species
from core.repository.species_repository import SpeciesRepository


class SpeciesSQLRepository(SpeciesRepository):
    def __init__(self, dao=None):
        self.dao = dao or SpeciesSQLDAO()

    def create(self, entity: Species):
        return self.dao.create(entity)

    def update(self, entity: Species):
        return self.dao.update(entity)

    def findOne(self, filters: dict):
        return self.dao.get_all(1, 0, filters)

    def find(self, length=20, offset=0, filters=None):
        filters = filters if filters else {}
        in_season = None
        if "in_season" in filters:
            in_season = filters["in_season"]
            del filters["in_season"]
        if "popular_name" in filters:
            value = filters["popular_name"]
            del filters["popular_name"]
            filters["popular_names"] = ["@>", '{"' + value + '"}']
        if in_season is None:
            return self.dao.get_all(filters=filters)
        else:
            filters_, query_params = self.dao._generate_filters(
                filters=filters)
            season_start = self.dao.fields['season_start_month']
            season_end = self.dao.fields['season_end_month']
            start_is_before_end = f"{season_start} <= {season_end}"
            start_is_not_before_end = f"{season_start} > {season_end}"
            filters_ += f" AND (({start_is_before_end} AND {season_start} <= " \
                        f"%s AND {season_end} >= " \
                        f"%s) OR ({start_is_not_before_end} AND " \
                        f"({season_start} <= %s OR {season_end} >= %s)))"
            query_params.extend([datetime.datetime.now().month] * 4)
            return self.dao.get_all_by_custom_query(filters_, query_params,
                                                    length, offset)

    def findById(self, _id: str):
        return self.dao.get(_id)

    def delete(self, _id: str):
        return self.dao.remove(filters={"id_": _id})


class SpeciesSQLDAO(GenericSQLDAO):
    table = 'species'
    FILTER = "{column} {comparator}{arg}"

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
        self.database.ALLOWED_COMPARATORS.append('IN')

    def _generate_filters(self, filters: dict) -> (str, list[str]):
        if filters is None:
            raise ValueError("No filters where passed! Filters must be a dict "
                             "with param names, expected values and "
                             "comparators in this form: "
                             "{'param':['comparator', 'value']} "
                             "or {'param': 'value'} for equality.")

        if not isinstance(filters, dict):
            raise TypeError("Filters where passed not as dict!"
                            " Filters must be a dict "
                            "with param names, expected values and "
                            "comparators in this form: "
                            "{'param':['comparator', 'value']} "
                            "or {'param': 'value'} for equality.")
        query_params = []
        for param in filters.values():
            if not isinstance(param, list):
                query_params.append(param)
            else:
                if not isinstance(param[1], list):
                    query_params.append(param[1])
                else:
                    query_params.extend(param[1])

        field_keys = self.fields.keys()
        for property_, value in filters.items():
            if property_ not in field_keys:
                self.logger.error("Property %s not available in %s for "
                                  "get_all.",
                                  property_,
                                  self.return_class.__name__)
                raise ValueError(
                    f"Property {property_} not available "
                    f"in {self.return_class.__name__}."
                )
            if isinstance(value, list) \
                    and value[0] not in self.database.ALLOWED_COMPARATORS:
                self.logger.error("Comparator %s not available in %s for "
                                  "get_all.",
                                  value[0],
                                  self.return_class.__name__)
                raise ValueError(
                    f"Comparator {value[0]} not allowed "
                    f"for {self.return_class.__name__}"
                )

        filters_for_query =[]
        for filter_ in filters.keys():
            comparator = filters[filter_][0] \
            if isinstance(filters[filter_], list) \
            else '='
            column = self.fields[filter_]
            arg = " %s" if comparator != 'IN' else " (" + ", ".join(["%s"] * (len(filters[filter_][1]))) + ")"
            filter_format = self.FILTER.format(column=column, comparator=comparator, arg=arg)
            filters_for_query.append(filter_format)

        filters_ = self.database.FILTERS.format(
            filters=' AND '.join(filters_for_query))

        return filters_, query_params

    def get_all_by_custom_query(self, filters, params, length=20, offset=0):
        query = self.database.SELECT_QUERY.format(
            fields=', '.join(self.fields.values()),
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
