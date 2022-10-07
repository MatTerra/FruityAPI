from dependency_injector.wiring import Provide, inject
from pydantic import ValidationError
from pytest import raises

from core.entity.species import Species
from core.repository.species_repository import SpeciesRepository
from core.usecase.approve_species import ApproveSpecies, ApproveSpeciesInput
from infra.exceptions import SpeciesAlreadyApprovedException
from infra.repository import RepositoryContainer
from infra.repository.species_memory_repository import SpeciesMemoryRepository
from test import container


class TestApproveSpecies:
    def test_shouldnt_accept_extra_args(self):
        test = {"extra": 1, "species": "a", "approver": "a"}
        assert ApproveSpeciesInput(**test).__dict__.get("extra") is None

    async def test_should_update_species_on_repository(self):
        repository = SpeciesMemoryRepository()
        with container.species.override(repository):
            species = Species(creator="tester")
            repository.create(species)
            assert repository.findOne(
                {"creator": "tester", "approved": False}) == species

            approveSpecies = ApproveSpecies()
            await approveSpecies.execute(
                ApproveSpeciesInput(approver="admin",
                                    species=species.id_))

            assert repository.findOne(
                {"creator": "tester", "approved": True,
                 "approved_by": "admin"}) is not None
            assert species.scientific_name == ""

    async def test_should_raise_if_species_approved(self):
        repository = SpeciesMemoryRepository()
        with container.species.override(repository):
            repository.database = dict()
            species = Species(creator="tester")
            species.approve("tester")
            repository.create(species)
            assert repository.findOne(
                {"creator": "tester", "approved": True}) == species

            approveSpecies = ApproveSpecies()
            with raises(SpeciesAlreadyApprovedException):
                await approveSpecies.execute(
                    ApproveSpeciesInput(approver="admin",
                                        species=species.id_))
