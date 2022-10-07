from dataclasses import dataclass, field
from typing import Optional

from dependency_injector.wiring import Provide

from core.repository.species_repository import SpeciesRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class FindSpeciesInput(UseCaseInput):
    scientific_name: Optional[str]
    popular_name: Optional[str]


class FindSpecies(UseCase):
    def __init__(
            self,
            repository: SpeciesRepository = Provide[
                RepositoryContainer.species]
    ):
        self.repository = repository

    async def execute(self, _input: UseCaseInput):
        input_filters = {filter: value
                         for filter, value in _input.__dict__.items()
                         if value is not None}
        return self.repository.find(filters={"approved": True,
                                             **input_filters})
