from typing import Optional

from dependency_injector.wiring import Provide

from core.repository.tree_repository import TreeRepository
from core.usecase import UseCase, UseCaseInput
from infra.repository import RepositoryContainer


class FindTreesInput(UseCaseInput):
    near: Optional[list[float]]
    producing: Optional[bool]
    in_season: Optional[bool]
    length: Optional[int] = 10
    offset: Optional[int] = 0


class FindTrees(UseCase):
    def __init__(
            self,
            repository: TreeRepository = Provide[
                RepositoryContainer.tree]
    ):
        self.repository = repository

    async def execute(self, _input: FindTreesInput):
        length = _input.length
        del _input.length
        offset = _input.offset
        del _input.offset
        input_filters = {_filter: value
                         for _filter, value in _input.__dict__.items()
                         if value is not None}
        return self.repository.find(filters={**input_filters}, length=length, offset=offset)
