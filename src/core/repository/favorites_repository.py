from abc import abstractmethod
from typing import Optional

from core.entity.favorites import Favorites


class FavoritesRepository:
    @abstractmethod
    def create(self, entity: Favorites) -> str:
        pass

    @abstractmethod
    def update(self, entity: Favorites) -> str:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> Optional[Favorites]:
        pass

    @abstractmethod
    def delete(self, entity: Favorites) -> int:
        pass