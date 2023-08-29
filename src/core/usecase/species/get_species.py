from dependency_injector.wiring import Provide

from core.repository.species_repository import SpeciesRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class GetSpeciesInput(UseCaseInput):
    species: str = ...


class GetSpecies(UseCase):
    def __init__(
            self,
            repository: SpeciesRepository = Provide[
                RepositoryContainer.species]
    ):
        self.repository = repository

    async def execute(self, _input: GetSpeciesInput):
        return self.repository.findById(_input.species)
