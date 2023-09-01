from typing import Optional
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from pydantic import BaseModel, validator

from core.entity.tree import Tree
from core.repository.tree_repository import TreeRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class CreateTreeRequestInput(BaseModel):
    species: Optional[str] = ""
    variety: Optional[str] = ""
    description: Optional[str] = ""
    location: Optional[tuple[float, float]] = ()
    pictures_url: Optional[list[str]] = []
    producing: Optional[bool] = False


class CreateTreeInput(UseCaseInput):
    creator: str = ...
    species: Optional[str] = ""
    variety: Optional[str] = ""
    description: Optional[str] = ""
    location: Optional[list[float]] = ()
    pictures_url: Optional[list[str]] = []
    producing: Optional[bool] = False

    @validator('pictures_url')
    def check_is_list(cls, v):
        assert isinstance(v, list) if v is not None else True
        return v

    @validator('creator', 'variety')
    def check_is_str(cls, v):
        assert isinstance(v, str) if v is not None else True
        return v

    @validator('species')
    def check_is_uuid(cls, v):
        try:
            assert isinstance(v, str) and UUID(v, version=4)
        except ValueError:
            assert False
        return v

    @validator('producing')
    def check_is_bool(cls, v):
        assert isinstance(v, bool) if v is not None else True
        return v

    @validator('description')
    def check_length_and_type(cls, v):
        assert isinstance(v, str) and len(v) <= 255 if v is not None else True
        return v

    @validator('location')
    def check_is_tuple(cls, v):
        assert isinstance(v, list) and len(v) == 2 if v is not None else True
        return tuple(v)


class CreateTree(UseCase):

    @inject
    def __init__(
            self,
            repository: TreeRepository = Provide[
                RepositoryContainer.tree]
    ):
        self.repository = repository

    async def execute(self, _input: CreateTreeInput):
        tree = Tree(**_input.__dict__)

        self.repository.create(tree)

        return tree.id_
