from typing import Optional

from dependency_injector.wiring import Provide

from core.repository.favorites_repository import FavoritesRepository
from core.repository.species_repository import SpeciesRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class FindSpeciesInput(UseCaseInput):
    scientific_name: Optional[str]
    popular_name: Optional[str]
    in_season: Optional[bool]
    length: Optional[int] = 10
    offset: Optional[int] = 0
    user: Optional[str] = None


class FindSpecies(UseCase):
    def __init__(
            self,
            repository: SpeciesRepository = Provide[
                RepositoryContainer.species],
            favorite_repository: FavoritesRepository = Provide[
                RepositoryContainer.favorite
            ]
    ):
        self.repository = repository
        self.favorite_repository = favorite_repository

    async def execute(self, _input: FindSpeciesInput):
        length = _input.length
        offset = _input.offset
        del _input.length
        del _input.offset
        input_filters = {_filter: value
                         for _filter, value in _input.__dict__.items()
                         if value is not None}
        species = self.repository.find(filters={"approved": True, **input_filters}, length=length, offset=offset)
        if _input.user is None:
            return species

        user_favorites = self.favorite_repository.find_by_user_id(_input.user)
        if user_favorites is None:
            return species

        favorite_species = user_favorites.species
        for species_ in species[1]:
            species_.favorite = species_.id_ in favorite_species

        return species
