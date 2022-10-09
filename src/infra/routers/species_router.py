from fastapi import APIRouter

from core.usecase.approve_species import ApproveSpecies, ApproveSpeciesInput
from core.usecase.find_species import FindSpecies, FindSpeciesInput
from core.usecase.propose_species import ProposeSpecies, ProposeSpeciesInput
from infra.exceptions import treat_exceptions

species_v1_router = APIRouter(
    prefix="/v1/species",
    tags=["species"]
)


@species_v1_router.get("/")
@treat_exceptions
def find_species(filters: FindSpeciesInput):
    find_species_handler = FindSpecies()
    return find_species_handler.execute(filters)


@species_v1_router.post("/")
@treat_exceptions
def find_species(values: ProposeSpeciesInput):
    find_species_handler = ProposeSpecies()
    return find_species_handler.execute(values)


@species_v1_router.post("/{species_id}/approve")
@treat_exceptions
def find_species(species_id: str):
    find_species_handler = ApproveSpecies()
    return find_species_handler.execute(
        ApproveSpeciesInput(species=species_id,
                            approver="test")
    )
