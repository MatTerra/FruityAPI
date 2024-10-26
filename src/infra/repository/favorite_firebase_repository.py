import logging
from typing import Optional

from firebase_admin import firestore
from nova_api.exceptions import NotEntityException, DuplicateEntityException

from core.entity.favorites import Favorites
from core.repository.favorites_repository import FavoritesRepository


class FavoriteFirebaseRepository(FavoritesRepository):
    def __init__(self):
        self.database = firestore.client().collection("favorites")
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

        self.update(entity)
        return entity.user

    def update(self, entity: Favorites) -> str:
        if not isinstance(entity, self.return_class):
            self.logger.error("Entity was not passed as an instance to update."
                              " Value received: %s", str(entity))
            raise NotEntityException(
                debug=f"Entity must be a {self.return_class.__name__} object! "
                      f"Entity was a {entity.__class__.__name__} object."
            )

        self.database.document(entity.user).set(entity.as_dict())
        return entity.user

    def find_by_user_id(self, user_id: str) -> Optional[Favorites]:
        favorites_ = self.database.document(user_id).get().to_dict()
        if favorites_ is None:
            return None
        favorites = Favorites(user=user_id)
        favorites.species |= set(favorites_.get("species", []))
        favorites.trees |= set(favorites_.get("trees", []))
        return favorites

    def delete(self, entity: Favorites) -> int:
        doc = self.database.document("tester").get()
        if doc.exists:
            doc.reference.delete()
        return 1
