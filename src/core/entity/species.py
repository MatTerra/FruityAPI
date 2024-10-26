from dataclasses import dataclass, field

from nova_api import Entity

from infra.exceptions import SpeciesAlreadyApprovedException


def is_valid_month(month: int):
    return 0 < month < 13 if month is not None else True


@dataclass
class Species(Entity):
    creator: str = field(default="")
    approved: bool = field(default=False)
    approved_by: str = field(default="")
    scientific_name: str = field(default="")
    popular_names: list = field(default_factory=list)
    description: str = field(default="",
                             metadata={"type": "VARCHAR(256)"})
    links: list = field(default_factory=list)
    pictures_url: list = field(default_factory=list)
    season_start_month: int = field(default=None,
                                    metadata={"validation": is_valid_month})
    season_end_month: int = field(default=None,
                                  metadata={"validation": is_valid_month})
    favorite: bool = field(default=False,
                           metadata={"database": False})

    def __post_init__(self):
        if isinstance(self.popular_names, str):
            self.popular_names = Species.parse_db_array(self.popular_names)
        if isinstance(self.links, str):
            self.links = Species.parse_db_array(self.links)
        if isinstance(self.pictures_url, str):
            self.pictures_url = Species.parse_db_array(self.pictures_url)

    @staticmethod
    def parse_db_array(array):
        db_array = array.strip().replace('{', '').replace('}', '').split(',')
        return list(filter(lambda v: v != "", map(lambda v: v.strip(), db_array)))

    def approve(self, approver: str) -> None:
        """
        Sets the species as approved and registers the approver.

        :param approver: User ID of the approver
        :return: None
        """
        if self.approved:
            raise SpeciesAlreadyApprovedException(
                debug=f"Species approved by {self.approved_by}")
        self.approved = True
        self.approved_by = approver

    def is_in_season_in_month(self, month: int) -> bool:
        """
        Checks if the species is in season in a given month

        :param month: month to check
        :return: true if in season, false otherwise
        """
        if self.season_start_month and self.season_end_month:
            month_is_in_between_start_and_end = self.season_start_month \
                                                <= month \
                                                <= self.season_end_month
            start_is_before_end = self.season_start_month <= \
                                  self.season_end_month
            return ((start_is_before_end and month_is_in_between_start_and_end)
                    or (not start_is_before_end
                        and (self.season_start_month <= month
                             or month <= self.season_end_month)))
        return False
