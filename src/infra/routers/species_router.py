from fastapi import APIRouter, Depends

from core.usecase.approve_species import ApproveSpecies, ApproveSpeciesInput
from core.usecase.find_species import FindSpecies, FindSpeciesInput
from core.usecase.propose_species import ProposeSpecies, \
    ProposeSpeciesInput, ProposeSpeciesRequestInput
from infra.authentication import get_user
from infra.exceptions import treat_exceptions

species_v1_router = APIRouter(
    prefix="/v1/species",
    tags=["species"]
)


@species_v1_router.get("/")
@treat_exceptions
def find_species(popular_name: str | None = None,
                 scientific_name: str | None = None):
    filters = FindSpeciesInput()
    filters.scientific_name = scientific_name
    filters.popular_name = popular_name
    find_species_handler = FindSpecies()
    return find_species_handler.execute(filters)


@species_v1_router.post("/")
@treat_exceptions
def find_species(values: ProposeSpeciesRequestInput, user=Depends(get_user)):
    find_species_handler = ProposeSpecies()
    input = ProposeSpeciesInput(**values.__dict__, creator=user.get("sub"))
    return find_species_handler.execute(input)


@species_v1_router.post("/{species_id}/approve")
@treat_exceptions
def find_species(species_id: str):
    find_species_handler = ApproveSpecies()
    return find_species_handler.execute(
        ApproveSpeciesInput(species=species_id,
                            approver="test")
    )
