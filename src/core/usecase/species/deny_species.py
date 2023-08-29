from dependency_injector.wiring import Provide, inject
from nova_api import NovaAPIException

from core.repository.species_repository import SpeciesRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class DenySpeciesInput(UseCaseInput):
    species: str
    denier: str

    def __post_init__(self):
        if self.denier is None:
            raise ValueError("Must inform denier!")
        if self.species is None:
            raise ValueError("Must inform species!")


@inject
class DenySpecies(UseCase):
    def __init__(
            self,
            repository: SpeciesRepository = Provide[
                RepositoryContainer.species]
    ):
        self.repository = repository

    async def execute(self, _input: DenySpeciesInput):
        species = self.repository.findById(_input.species)

        if species.approved:
            raise NovaAPIException(status_code=422, message="Species already approved")

        self.repository.delete(species.id_)
