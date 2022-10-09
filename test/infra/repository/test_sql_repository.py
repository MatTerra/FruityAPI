from pytest import raises

from infra.repository.species_sql_repository import SpeciesSQLRepository


class TestSQLRepository:
    def test_can_init(self):
        with raises(ConnectionError):
            SpeciesSQLRepository()
