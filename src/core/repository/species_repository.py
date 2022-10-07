from abc import abstractmethod
from typing import Optional

from core.entity.species import Species
from core.repository import Repository


class SpeciesRepository(Repository):
    @abstractmethod
    def create(self, entity: Species) -> str:
        pass

    @abstractmethod
    def update(self, entity: Species) -> str:
        pass

    @abstractmethod
    def findOne(self, filters: dict) -> Optional[Species]:
        pass

    @abstractmethod
    def find(self, length=20, offset=0, filters: dict = dict()) \
            -> (int, list[Species]):
        pass

    @abstractmethod
    def findById(self, _id: str) -> Optional[Species]:
        pass

    @abstractmethod
    def delete(self, _id: str) -> int:
        pass

