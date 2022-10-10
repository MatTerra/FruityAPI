from nova_api.exceptions import InvalidAttributeException
from pytest import raises, mark

from core.entity.species import Species
from infra.exceptions import SpeciesAlreadyApprovedException


class TestSpecies:
    def test_approve_should_register_approver(self):
        species = Species()
        species.approve("admin")
        assert species.approved is True
        assert species.approved_by == "admin"

    def test_shouldnt_accept_month_out_of_range(self):
        with raises(InvalidAttributeException):
            Species(season_start_month=0, season_end_month=13)

        species = Species()

        with raises(InvalidAttributeException):
            species.season_start_month = 13
        with raises(InvalidAttributeException):
            species.season_end_month = 0

    @mark.parametrize("month", [*range(1,13), None])
    def test_should_accept_valid_month(self, month):
        Species(season_start_month=month, season_end_month=month)

    def test_approve_should_set_approved(self):
        species = Species()
        species.approve("admin")
        assert species.approved is True
        assert species.approved_by == "admin"

    def test_approve_should_raise_if_already_approved(self):
        species = Species()
        species.approve("admin")
        with raises(SpeciesAlreadyApprovedException):
            species.approve("tester")
