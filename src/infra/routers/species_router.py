from fastapi import APIRouter, Depends, HTTPException

from core.usecase.species.approve_species import ApproveSpecies, ApproveSpeciesInput
from core.usecase.species.deny_species import DenySpecies, DenySpeciesInput
from core.usecase.species.favorite_species import FavoriteSpeciesRequestInput, FavoriteSpecies, FavoriteSpeciesInput
from core.usecase.species.find_species import FindSpecies, FindSpeciesInput
from core.usecase.species.get_species import GetSpecies, GetSpeciesInput
from core.usecase.species.list_unapproved_species import ListUnapprovedSpeciesInput, ListUnapprovedSpecies
from core.usecase.species.list_user_proposals import ListUserProposalsSpeciesInput, ListUserProposalsSpecies
from core.usecase.species.propose_species import ProposeSpecies, \
    ProposeSpeciesInput, ProposeSpeciesRequestInput
from core.usecase.species.unfavorite_species import UnfavoriteSpeciesInput, UnfavoriteSpecies, \
    UnfavoriteSpeciesRequestInput
from infra.authentication import get_user, optional_get_user
from infra.exceptions import treat_exceptions

species_v1_router = APIRouter(
    prefix="/v1/species",
    tags=["species"]
)


@species_v1_router.get("")
@treat_exceptions
def find_species(popular_name: str | None = None,
                 scientific_name: str | None = None,
                 length: int = 10,
                 offset: int = 0,
                 user=Depends(optional_get_user)):
    filters = FindSpeciesInput(length=length, offset=offset, user=user.get("sub"))
    filters.scientific_name = scientific_name
    filters.popular_name = popular_name
    find_species_handler = FindSpecies()
    return find_species_handler.execute(filters)


@species_v1_router.get("/my-species")
@treat_exceptions
def find_my_proposals_species(approved: bool | None = None,
                              user=Depends(get_user)):
    filters = ListUserProposalsSpeciesInput(
        creator=user.get("sub")
    )
    filters.approved = approved
    list_user_proposals_species_handler = ListUserProposalsSpecies()
    return list_user_proposals_species_handler.execute(filters)


@species_v1_router.get("/pending")
@treat_exceptions
def find_species(popular_name: str | None = None,
                 scientific_name: str | None = None,
                 user=Depends(get_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403,
                            detail="Only admins can list pending species")
    filters = ListUnapprovedSpeciesInput()
    filters.scientific_name = scientific_name
    filters.popular_name = popular_name
    find_species_handler = ListUnapprovedSpecies()
    return find_species_handler.execute(filters)


@species_v1_router.post("")
@treat_exceptions
def propose_species(values: ProposeSpeciesRequestInput,
                    user=Depends(get_user)):
    propose_species_handler = ProposeSpecies()
    _input = ProposeSpeciesInput(**values.__dict__, creator=user.get("sub"))
    return propose_species_handler.execute(_input)


@species_v1_router.post("/favorite")
@treat_exceptions
def favorite_species(values: FavoriteSpeciesRequestInput,
                    user=Depends(get_user)):
    favorite_species_handler = FavoriteSpecies()
    _input = FavoriteSpeciesInput(**values.__dict__, user=user.get("sub"))
    return favorite_species_handler.execute(_input)


@species_v1_router.post("/unfavorite")
@treat_exceptions
def unfavorite_species(values: UnfavoriteSpeciesRequestInput,
                    user=Depends(get_user)):
    unfavorite_species_handler = UnfavoriteSpecies()
    _input = UnfavoriteSpeciesInput(**values.__dict__, creator=user.get("sub"))
    return unfavorite_species_handler.execute(_input)


@species_v1_router.post("/{species_id}/approve")
@treat_exceptions
def approve_species(species_id: str,
                    user=Depends(get_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403,
                            detail="Only admins can approve species")
    approve_species_handler = ApproveSpecies()
    return approve_species_handler.execute(
        ApproveSpeciesInput(species=species_id,
                            approver=user.get("sub"))
    )


@species_v1_router.post("/{species_id}/deny")
@treat_exceptions
def approve_species(species_id: str,
                    user=Depends(get_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403,
                            detail="Only admins can deny species")
    deny_species_handler = DenySpecies()
    return deny_species_handler.execute(
        DenySpeciesInput(species=species_id,
                         denier=user.get("sub")))


@species_v1_router.get("/{species_id}")
@treat_exceptions
def find_species(species_id: str):
    get_species_handler = GetSpecies()
    return get_species_handler.execute(
        GetSpeciesInput(species=species_id)
    )
