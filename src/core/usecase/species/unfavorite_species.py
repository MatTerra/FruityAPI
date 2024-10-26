from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from core.entity.favorites import Favorites
from core.repository.favorites_repository import FavoritesRepository
from core.usecase import UseCaseInput, UseCase
from infra.repository import RepositoryContainer


class UnfavoriteSpeciesRequestInput(BaseModel):
    species: str


class UnfavoriteSpeciesInput(UseCaseInput):
    species: str
    user: str

    def __post_init__(self):
        if self.user is None:
            raise ValueError("Must inform user!")
        if self.species is None:
            raise ValueError("Must inform species!")


@inject
class UnfavoriteSpecies(UseCase):
    def __init__(
            self,
            repository: FavoritesRepository = Provide[RepositoryContainer.favorite]
    ):
        self.repository = repository

    async def execute(self, _input: UnfavoriteSpeciesInput):
        favorite = self.repository.find_by_user_id(_input.user) or Favorites(
            user=_input.user
        )
        favorite.species.remove(_input.species)
        return self.repository.update(favorite)
