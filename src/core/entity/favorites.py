from dataclasses import field, dataclass


@dataclass
class Favorites:
    user: str
    species: set[str] = field(default_factory=set)
    trees: set[str] = field(default_factory=set)

    def as_dict(self):
        return {"species": self.species, "trees": self.trees}
