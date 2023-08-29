from typing import Optional

from dependency_injector.wiring import Provide

from core.repository.species_repository import SpeciesRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class ListUserProposalsSpeciesInput(UseCaseInput):
    creator: str
    approved: Optional[bool]


class ListUserProposalsSpecies(UseCase):
    def __init__(
            self,
            repository: SpeciesRepository = Provide[
                RepositoryContainer.species]
    ):
        self.repository = repository

    async def execute(self, _input: ListUserProposalsSpeciesInput):
        input_filters = {_filter: value
                         for _filter, value in _input.__dict__.items()
                         if value is not None}
        return self.repository.find(filters={**input_filters})
