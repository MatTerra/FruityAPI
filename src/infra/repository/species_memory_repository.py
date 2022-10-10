import logging
import datetime
from copy import deepcopy
from typing import Optional

from nova_api.exceptions import DuplicateEntityException, \
    EntityNotFoundException, NotEntityException

from core.entity.species import Species
from core.repository.species_repository import SpeciesRepository


class SpeciesMemoryRepository(SpeciesRepository):
    def __init__(self):
        self.database = {}
        self.logger = logging.getLogger()
        self.return_class = Species

    def create(self, entity: Species) -> str:
        if not isinstance(entity, self.return_class):
            self.logger.error("Entity was not passed as an instance to create."
                              " Value received: %s", str(entity))
            raise NotEntityException(
                debug=f"Entity must be a {self.return_class.__name__} object! "
                      f"Entity was a {entity.__class__.__name__} object."
            )

        if self.findById(entity.id_) is not None:
            self.logger.error("Entity was found in database before create."
                              " Value received: %s", str(entity))
            raise DuplicateEntityException(
                debug=f"{self.return_class.__name__} uuid {entity.id_} "
                      f"already exists in database!"
            )
        self.database[entity.id_] = deepcopy(entity)
        return entity.id_

    def update(self, entity: Species) -> str:
        if not isinstance(entity, self.return_class):
            self.logger.error("Entity was not passed as an instance to update."
                              " Value received: %s", str(entity))
            raise NotEntityException(
                debug=f"Entity must be a {self.return_class.__name__} object! "
                      f"Entity was a {entity.__class__.__name__} object."
            )

        if self.database.get(entity.id_) is None:
            self.logger.error("Entity was not found in database to update."
                              " Value received: %s", str(entity))
            raise EntityNotFoundException(debug=f"Entity id_ is {entity.id_}")

        self.database[entity.id_] = deepcopy(entity)
        return entity.id_

    def findOne(self, filters: dict) -> Optional[Species]:
        for _id, species in self.database.items():
            for property, value in filters.items():
                if species.__dict__[property] != value:
                    break
            else:
                return species
        return None

    def find(self, length=20, offset=0, filters: dict = None) \
            -> (int, list[Species]):
        results = []
        for _id, species in self.database.items():
            for _property, value in filters.items():
                in_season = species.is_in_season_in_month(
                    datetime.datetime.now().month
                )
                if _property == "in_season" and in_season is not value:
                    break
                if _property == "popular_name" and \
                        value not in species.popular_names:
                    break
                if _property != "popular_name" and \
                        _property in species.__dict__ and \
                        species.__dict__[_property] != value:
                    break
            else:
                results.append(species)
        results = results[offset:length]
        return 0 if len(results) == 0 else len(self.database), results

    def findById(self, _id: str) -> Optional[Species]:
        return self.database.get(_id)

    def delete(self, _id: str) -> int:
        del self.database[_id]
        return 1
