from dataclasses import dataclass

from dependency_injector.wiring import Provide, inject

from core.repository.species_repository import SpeciesRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class ApproveSpeciesInput(UseCaseInput):
    species: str
    approver: str

    def __post_init__(self):
        if self.approver is None:
            raise ValueError("Must inform approver!")
        if self.species is None:
            raise ValueError("Must inform species!")


@inject
class ApproveSpecies(UseCase):
    def __init__(
            self,
            repository: SpeciesRepository = Provide[
                RepositoryContainer.species]
    ):
        self.repository = repository

    async def execute(self, _input: ApproveSpeciesInput):
        species = self.repository.findById(_input.species)

        species.approve(_input.approver)

        self.repository.update(species)
