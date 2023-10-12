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
async def check_health():
    find_species_handler = FindSpecies()
    await find_species_handler.execute(FindSpeciesInput(length=1))
    find_trees_handler = FindTrees()
    await find_trees_handler.execute(FindTreesInput(length=1))
    return {"status": "OK"}