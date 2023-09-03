from fastapi import APIRouter

from core.usecase.species.find_species import FindSpecies, FindSpeciesInput
from core.usecase.tree.find_trees import FindTrees, FindTreesInput
from infra.exceptions import treat_exceptions

health_v1_router = APIRouter(
    prefix="/v1/health",
    tags=["health"]
)


@health_v1_router.get("")
@treat_exceptions
def check_health():
    find_species_handler = FindSpecies()
    find_species_handler.execute(FindSpeciesInput())
    find_trees_handler = FindTrees()
    find_trees_handler.execute(FindTreesInput())
    return "OK"