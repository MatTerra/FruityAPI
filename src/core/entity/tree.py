import json
from dataclasses import dataclass, field

from nova_api import Entity

from core.entity.species import Species
from infra.exceptions import SpeciesAlreadyApprovedException


@dataclass
class Tree(Entity):
    creator: str = field(default="")
    species: Species = field(default=None)
    variety: str = field(default="")
    location: tuple = field(default_factory=tuple,
                            metadata={"type": "geography"})
    description: str = field(default="",
                             metadata={"type": "VARCHAR(256)"})
    producing: bool = field(default=False)
    pictures_url: list = field(default_factory=list)

    @staticmethod
    def tree_serializer(field_value):
        if isinstance(field_value, tuple):
            return f"POINT{str(field_value).replace(',', '')}"
        return Entity.serialize_field(field_value)

    def get_db_values(self, field_serializer=None) -> list:
        return super().get_db_values(Tree.tree_serializer)

    def __post_init__(self):
        if isinstance(self.pictures_url, str):
            self.pictures_url = self.parse_db_array(self.pictures_url)
        if isinstance(self.location, str):
            self.location = Tree.parse_db_location(self.location)

    @staticmethod
    def parse_db_array(array):
        db_array = array.strip().replace('{', '').replace('}', '').split(',')
        return list(filter(lambda v: v != '', map(lambda v: v.strip(), db_array)))

    @staticmethod
    def parse_db_location(tuple_) -> tuple:
        return tuple(json.loads(tuple_).get('coordinates', tuple))
