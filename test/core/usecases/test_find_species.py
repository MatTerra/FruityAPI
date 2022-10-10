import datetime
from unittest.mock import MagicMock

from pytest import fixture

from core.entity.species import Species
from core.usecase.find_species import FindSpecies, FindSpeciesInput
from infra.repository.species_memory_repository import SpeciesMemoryRepository
from test import container


class TestFindSpecies:
    @fixture
    def cagaita(self):
        return Species(popular_names=["cagaita"],
                       scientific_name="eugenia dysenterica",
                       approved=True,
                       approved_by="admin",
                       creator="tester",
                       season_start_month=9,
                       season_end_month=10)

    @fixture
    def cajuzinho(self):
        return Species(popular_names=["cajuzinho do cerrado", "caju anão"],
                       scientific_name="anacardium humile",
                       approved=True,
                       approved_by="admin2",
                       creator="admin",
                       season_start_month=10,
                       season_end_month=12)

    @fixture
    def not_approved(self):
        return Species(popular_names=["algo"],
                       creator="user")

    async def test_find_species_without_filter_shouldnt_return_non_approved(
            self,
            cagaita,
            cajuzinho,
            not_approved
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(not_approved)
        with container.species.override(repository):
            find_species = FindSpecies()
            results = await find_species.execute(FindSpeciesInput())
            assert results == (3, [cagaita, cajuzinho])

    async def test_find_species_with_scientific_name_should_return(
            self,
            cagaita,
            cajuzinho,
            not_approved
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(not_approved)
        with container.species.override(repository):
            find_species = FindSpecies()
            results = await find_species.execute(FindSpeciesInput(
                scientific_name="eugenia dysenterica"
            ))
            assert results == (3, [cagaita])

    async def test_find_with_scientific_name_shouldnt_return_if_not_found(
            self,
            cagaita,
            cajuzinho,
            not_approved
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(not_approved)
        with container.species.override(repository):
            find_species = FindSpecies()
            results = await find_species.execute(FindSpeciesInput(
                scientific_name="eugenia bela"
            ))
            assert results == (0, [])

    async def test_find_species_with_popular_name_should_return(
            self,
            cagaita,
            cajuzinho,
            not_approved
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(not_approved)
        with container.species.override(repository):
            find_species = FindSpecies()
            results = await find_species.execute(FindSpeciesInput(
                popular_name="cagaita"
            ))
            assert results == (3, [cagaita])

    async def test_find_species_in_season_should_return(
            self,
            cagaita,
            cajuzinho,
            not_approved,
            monkeypatch
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(not_approved)
        datetime_mock = MagicMock(wrap=datetime.datetime)
        datetime_mock.now.return_value = datetime.datetime(
            2022, 9, 10, 0, 0, 0)
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        with container.species.override(repository):
            find_species = FindSpecies()
            results = await find_species.execute(FindSpeciesInput(
                in_season=True
            ))
            assert results == (3, [cagaita])

    async def test_find_species_not_in_season_should_return(
            self,
            cagaita,
            cajuzinho,
            not_approved,
            monkeypatch
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(not_approved)
        datetime_mock = MagicMock(wrap=datetime.datetime)
        datetime_mock.now.return_value = datetime.datetime(
            2022, 9, 10, 0, 0, 0)
        monkeypatch.setattr(datetime, "datetime", datetime_mock)
        with container.species.override(repository):
            find_species = FindSpecies()
            results = await find_species.execute(FindSpeciesInput(
                in_season=False
            ))
            assert results == (3, [cajuzinho])
