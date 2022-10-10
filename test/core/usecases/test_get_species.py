import datetime
from unittest.mock import MagicMock

from pydantic import ValidationError
from pytest import fixture, raises

from core.entity.species import Species
from core.usecase.get_species import GetSpecies, GetSpeciesInput
from infra.repository.species_memory_repository import SpeciesMemoryRepository
from test import container

class TestGetSpeciesInput:
    def test_should_raise_if_no_id(self):
        with raises(ValidationError):
            GetSpeciesInput()


class TestGetSpecies:
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

    async def test_get_species_exist_should_return(
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
            get_species = GetSpecies()
            results = await get_species.execute(GetSpeciesInput(
                species=cagaita.id_
            ))
            assert results == cagaita

    async def test_get_species_non_approved_should_return(
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
            get_species = GetSpecies()
            results = await get_species.execute(GetSpeciesInput(
                species=not_approved.id_
            ))
            assert results == not_approved

    async def test_get_shouldnt_return_if_not_found(
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
            get_species = GetSpecies()
            results = await get_species.execute(GetSpeciesInput(
                species="eugenia bela"
            ))
            assert results is None