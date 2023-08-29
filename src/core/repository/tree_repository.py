from abc import abstractmethod
from typing import Optional

from core.entity.species import Species
from core.entity.tree import Tree
from core.repository import Repository


class TreeRepository(Repository):
    @abstractmethod
    def create(self, entity: Tree) -> str:
        pass

    @abstractmethod
    def update(self, entity: Tree) -> str:
        pass

    @abstractmethod
    def findOne(self, filters: dict) -> Optional[Tree]:
        pass

    @abstractmethod
    def find(self, length=20, offset=0, filters: dict = dict()) \
            -> (int, list[Tree]):
        pass

    @abstractmethod
    def findById(self, _id: str) -> Optional[Tree]:
        pass

    @abstractmethod
    def delete(self, _id: str) -> int:
        pass

