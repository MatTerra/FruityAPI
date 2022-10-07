from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from core.usecase.find_species import FindSpecies, FindSpeciesInput
from infra.exceptions import treat_exceptions
from infra.repository.species_sql_repository import SpeciesSQLRepository

species_v1_router = APIRouter(
    prefix="/v1/species",
    tags=["species"]
)


@cbv(species_v1_router)
class SpeciesV1Router:
    @species_v1_router.get("/")
    @treat_exceptions
    def find_species(self, filters: FindSpeciesInput):
        find_species_handler = FindSpecies(SpeciesSQLRepository())
        return find_species_handler.execute(filters)


