from abc import ABC, abstractmethod
from typing import Optional

from nova_api import Entity


class Repository(ABC):
    @abstractmethod
    def create(self, entity: Entity) -> str:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: Entity) -> str:
        raise NotImplementedError

    @abstractmethod
    def findOne(self, filters: dict) -> Optional[Entity]:
        raise NotImplementedError

    @abstractmethod
    def find(self, length: int = 20, offset: int = 0, filters: dict = None)\
            -> (int, list[Entity]):
        raise NotImplementedError

    @abstractmethod
    def findById(self, _id: str) -> Optional[Entity]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, _id: str) -> int:
        raise NotImplementedError
