from fastapi import APIRouter, Depends

from core.usecase.tree.create_tree import CreateTreeRequestInput, CreateTree, CreateTreeInput
from core.usecase.tree.find_trees import FindTreesInput, FindTrees
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


@tree_v1_router.get("")
@treat_exceptions
def find_trees(near: list[float] | None = None,
               producing: bool | None = None,
               in_season: bool | None = None,
               length: int = 10,
               offset: int = 0,
               ):
    filters = FindTreesInput(length=length, offset=offset)
    filters.near = near
    filters.producing = producing
    find_trees_handler = FindTrees()
    return find_trees_handler.execute(filters)
