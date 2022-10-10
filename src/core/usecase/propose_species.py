from typing import Optional

from dependency_injector.wiring import Provide, inject
from pydantic import BaseModel, validator

from core.entity.species import Species, is_valid_month
from core.repository.species_repository import SpeciesRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class ProposeSpeciesRequestInput(BaseModel):
    scientific_name: Optional[str] = ""
    popular_names: Optional[list[str]]
    description: Optional[str] = ""
    links: Optional[list[str]]
    pictures_url: Optional[list[str]]
    season_start_month: Optional[int]
    season_end_month: Optional[int]


class ProposeSpeciesInput(UseCaseInput):
    creator: str = ...
    scientific_name: Optional[str] = ""
    popular_names: Optional[list[str]] = None
    description: Optional[str] = ""
    links: Optional[list[str]] = None
    pictures_url: Optional[list[str]] = None
    season_start_month: Optional[int] = None
    season_end_month: Optional[int] = None

    @validator('season_start_month', 'season_end_month')
    def check_month(cls, v):
        assert is_valid_month(v)
        return v


class ProposeSpecies(UseCase):

    @inject
    def __init__(
            self,
            repository: SpeciesRepository = Provide[
                RepositoryContainer.species]
    ):
        self.repository = repository

    async def execute(self, _input: ProposeSpeciesInput):
        species = Species(**_input.__dict__)

        self.repository.create(species)

        return species.id_
