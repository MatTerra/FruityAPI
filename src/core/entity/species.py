from dataclasses import dataclass, field
from typing import List

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
    description: str = field(default="")
    links: list = field(default_factory=list)
    pictures_url: list = field(default_factory=list)
    season_start_month: int = field(default=None,
                                    metadata={"validation": is_valid_month})
    season_end_month: int = field(default=None,
                                  metadata={"validation": is_valid_month})

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
        if self.season_start_month and self.season_end_month:

            return self.season_start_month <= month <= self.season_end_month \
                if self.season_start_month < self.season_end_month \
                else self.season_start_month <= month \
                     or month <= self.season_end_month

        return False
