from pytest import fixture

from core.entity.species import Species
from core.usecase.species.list_unapproved_species import ListUnapprovedSpecies, ListUnapprovedSpeciesInput
from infra.repository.species_memory_repository import SpeciesMemoryRepository
from test import container


class TestListUnapprovedSpecies:
    @fixture
    def cagaita(self):
        return Species(popular_names=["cagaita"],
                       scientific_name="eugenia dysenterica",
                       approved=False,
                       creator="tester",
                       season_start_month=9,
                       season_end_month=10)

    @fixture
    def cajuzinho(self):
        return Species(popular_names=["cajuzinho do cerrado", "caju anão"],
                       scientific_name="anacardium humile",
                       approved=False,
                       creator="admin",
                       season_start_month=10,
                       season_end_month=12)

    @fixture
    def approved(self):
        return Species(popular_names=["algo"],
                       creator="user",
                       approved=True,
                       approved_by="admin")

    async def test_list_unapproved_species_without_filter_should_return_only_non_approved(
            self,
            cagaita,
            cajuzinho,
            approved
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(approved)
        with container.species.override(repository):
            list_unapproved_species = ListUnapprovedSpecies()
            results = await list_unapproved_species.execute(ListUnapprovedSpeciesInput())
            assert results == (3, [cagaita, cajuzinho])

    async def test_list_unapproved_species_with_scientific_name_should_return(
            self,
            cagaita,
            cajuzinho,
            approved
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(approved)
        with container.species.override(repository):
            list_unapproved_species = ListUnapprovedSpecies()
            results = await list_unapproved_species.execute(ListUnapprovedSpeciesInput(
                scientific_name="eugenia dysenterica"
            ))
            assert results == (3, [cagaita])

    async def test_find_with_scientific_name_shouldnt_return_if_not_found(
            self,
            cagaita,
            cajuzinho,
            approved
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(approved)
        with container.species.override(repository):
            list_unapproved_species = ListUnapprovedSpecies()
            results = await list_unapproved_species.execute(ListUnapprovedSpeciesInput(
                scientific_name="eugenia bela"
            ))
            assert results == (0, [])

    async def test_list_unapproved_species_with_popular_name_should_return(
            self,
            cagaita,
            cajuzinho,
            approved
    ):
        repository = SpeciesMemoryRepository()
        repository.create(cagaita)
        repository.create(cajuzinho)
        repository.create(approved)
        with container.species.override(repository):
            list_unapproved_species = ListUnapprovedSpecies()
            results = await list_unapproved_species.execute(ListUnapprovedSpeciesInput(
                popular_name="cagaita"
            ))
            assert results == (3, [cagaita])
