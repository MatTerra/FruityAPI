from pytest import fixture

from core.entity.species import Species
from core.usecase.find_species import FindSpecies, FindSpeciesInput
from infra.repository import RepositoryContainer
from infra.repository.species_memory_repository import SpeciesMemoryRepository
from test import container

class TestFindSpecies:
    @fixture
    def cagaita(self):
        return Species(popular_names=["cagaita"],
                       scientific_name="eugenia dysenterica",
                       approved=True,
                       approved_by="admin",
                       creator="tester")

    @fixture
    def cajuzinho(self):
        return Species(popular_names=["cajuzinho do cerrado", "caju anão"],
                       scientific_name="anacardium humile",
                       approved=True,
                       approved_by="admin2",
                       creator="admin")

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
            assert results == (2, [cagaita, cajuzinho])

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
            assert results == (1, [cagaita])

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
            assert results == (1, [cagaita])
