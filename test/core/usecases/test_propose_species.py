from pydantic import ValidationError
from pytest import mark, raises

from core.usecase.propose_species import ProposeSpecies, ProposeSpeciesInput
from infra.repository.species_memory_repository import SpeciesMemoryRepository

from test import container


class TestProposeSpeciesInput:
    def test_shouldnt_accept_empty_creator(self):
        with raises(ValidationError):
            _input = ProposeSpeciesInput()

    @mark.parametrize("month", [*range(1, 13), None])
    def test_should_accept_valid_month(self, month):
        _input = ProposeSpeciesInput(creator="test",
                                     season_start_month=month,
                                     season_end_month=month)

    @mark.parametrize("month", [0, 13])
    def test_shouldnt_accept_invalid_month(self, month):
        with raises(ValidationError):
            _input = ProposeSpeciesInput(creator="test",
                                         season_start_month=month,
                                         season_end_month=month)

    def test_should_accept_non_empty_creator(self):
        _input = ProposeSpeciesInput(creator="test")


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
