import logging
from copy import deepcopy
from typing import Optional

from nova_api.exceptions import NotEntityException, DuplicateEntityException

from core.entity.favorites import Favorites
from core.repository.favorites_repository import FavoritesRepository


class FavoriteMemoryRepository(FavoritesRepository):
    def __init__(self):
        self.database = {}
        self.logger = logging.getLogger()
        self.return_class = Favorites

    def create(self, entity: Favorites) -> str:
        if not isinstance(entity, self.return_class):
            self.logger.error("Entity was not passed as an instance to create."
                              " Value received: %s", str(entity))
            raise NotEntityException(
                debug=f"Entity must be a {self.return_class.__name__} object! "
                      f"Entity was a {entity.__class__.__name__} object."
            )
        if self.find_by_user_id(entity.user) is not None:
            self.logger.error("Entity was found in database before create."
                              " Value received: %s", str(entity))
            raise DuplicateEntityException(
                debug=f"{self.return_class.__name__} user {entity.user} "
                      f"already exists in database!"
            )

        self.database[entity.user] = deepcopy(entity)
        return entity.user

    def update(self, entity: Favorites) -> str:
        if not isinstance(entity, self.return_class):
            self.logger.error("Entity was not passed as an instance to update."
                              " Value received: %s", str(entity))
            raise NotEntityException(
                debug=f"Entity must be a {self.return_class.__name__} object! "
                      f"Entity was a {entity.__class__.__name__} object."
            )

        if self.database.get(entity.user) is None:
            return self.create(entity)

        self.database[entity.user].species = set(entity.species)
        self.database[entity.user].trees = set(entity.trees)
        return entity.user

    def find_by_user_id(self, user_id: str) -> Optional[Favorites]:
        favorites = self.database.get(user_id, None)
        return favorites

    def delete(self, entity: Favorites) -> int:
        del self.database[entity.user]
        return 1
