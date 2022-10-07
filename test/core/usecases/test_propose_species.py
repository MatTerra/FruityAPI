from core.usecase.propose_species import ProposeSpecies, ProposeSpeciesInput
from infra.repository.species_memory_repository import SpeciesMemoryRepository

from test import container


class TestProposeSpecies:
    def test_shouldnt_accept_extra_args(self):
        test = {"extra": 1, "creator": "Test"}
        assert ProposeSpeciesInput(**test).__dict__.get("extra") is None

    async def test_should_register_species_on_repository(self):
        repository = SpeciesMemoryRepository()
        with container.species.override(repository):
            proposeSpecies = ProposeSpecies()
            await proposeSpecies.execute(
                ProposeSpeciesInput(creator="admin",
                                    popular_names=["Cagaita"]))
            species = repository.findOne(
                {"creator": "admin", "popular_names": ["Cagaita"]})
            assert species is not None
            assert species.scientific_name == ""
