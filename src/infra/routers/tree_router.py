from fastapi import APIRouter, Depends

from core.usecase.tree.create_tree import CreateTreeRequestInput, CreateTree, CreateTreeInput
from infra.authentication import get_user
from infra.exceptions import treat_exceptions

tree_v1_router = APIRouter(
    prefix="/v1/tree",
    tags=["tree"]
)


@tree_v1_router.post("")
@treat_exceptions
def create_tree(values: CreateTreeRequestInput,
                user=Depends(get_user)):
    create_tree_handler = CreateTree()
    _input = CreateTreeInput(**values.__dict__, creator=user.get("sub"))
    return create_tree_handler.execute(_input)
