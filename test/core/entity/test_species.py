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

    @mark.parametrize("month", [*range(1, 13), None])
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

    @mark.parametrize("month", range(1, 13))
    def test_is_in_season_should_return_false_if_season_not_set(self,
                                                                month: int):
        assert Species().is_in_season_in_month(month) is False

    @mark.parametrize("month", range(1, 11))
    def test_is_in_season_if_start_before_and_end_after(
            self, month: int
    ):
        species = Species(season_start_month=month, season_end_month=month + 2)
        assert species.is_in_season_in_month(month + 1) is True

    @mark.parametrize("month", range(1, 12))
    def test_is_in_season_if_start_same_and_end_after(
            self, month: int
    ):
        species = Species(season_start_month=month, season_end_month=month + 1)
        assert species.is_in_season_in_month(month) is True

    @mark.parametrize("month", range(1, 12))
    def test_is_in_season_if_start_before_and_end_same(
            self, month: int
    ):
        species = Species(season_start_month=month, season_end_month=month + 1)
        assert species.is_in_season_in_month(month + 1) is True

    @mark.parametrize("month", range(1, 13))
    def test_is_in_season_if_start_and_end_same(
            self, month: int
    ):
        species = Species(season_start_month=month, season_end_month=month)
        assert species.is_in_season_in_month(month) is True

    def test_is_in_season_should_wrap(self):
        species = Species(season_start_month=11, season_end_month=2)
        assert species.is_in_season_in_month(12) is True
        assert species.is_in_season_in_month(1) is True

    def test_is_in_season_should_return_false_if_out_of_season(self):
        species = Species(season_start_month=11, season_end_month=2)
        assert species.is_in_season_in_month(10) is False
        assert species.is_in_season_in_month(3) is False
        species = Species(season_start_month=6, season_end_month=7)
        assert species.is_in_season_in_month(5) is False
        assert species.is_in_season_in_month(8) is False
