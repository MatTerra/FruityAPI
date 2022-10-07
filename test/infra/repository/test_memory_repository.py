import pytest
from nova_api.exceptions import DuplicateEntityException, \
    EntityNotFoundException, NotEntityException
from pytest import fixture, raises, mark

from core.entity.species import Species
from infra.repository.species_memory_repository import SpeciesMemoryRepository


class TestMemoryRepository:
    @fixture
    def repository(self):
        return SpeciesMemoryRepository()

    def test_init_should_create_empty_database(self, repository):
        assert repository.database == dict()

    def test_create_should_include_in_database(self, repository):
        species = Species(popular_names=["test"])
        assert repository.create(species) == species.id_
        assert repository.database == {species.id_: species}

    @mark.parametrize("arg", [
        "1243",
        dict(),
        list(),
        True,
        None
    ])
    def test_create_with_non_species_arg_should_throw(self, repository, arg):
        with raises(NotEntityException):
            repository.create(arg)

    def test_cant_duplicate_entry(self, repository):
        species = Species(creator="Tester")
        repository.create(species)
        assert repository.database == {species.id_: species}
        with raises(DuplicateEntityException):
            repository.create(species)

    def test_find_one_species_should_return_first_match(self, repository):
        species = Species(creator="Tester")
        repository.create(species)
        species2 = Species(creator="Tester")
        repository.create(species2)
        assert repository.database == {species.id_: species,
                                       species2.id_: species2}
        assert repository.findOne({"creator": "Tester"}) == species

    def test_find_one_species_should_return_none_if_no_match(self, repository):
        species = Species(creator="Tester")
        repository.create(species)
        species2 = Species(creator="Tester")
        repository.create(species2)
        assert repository.database == {species.id_: species,
                                       species2.id_: species2}
        assert repository.findOne({"creator": "Admin"}) is None

    def test_find_species_should_return_matches(self, repository):
        species = Species(creator="Tester")
        repository.create(species)
        species2 = Species(creator="Tester")
        repository.create(species2)
        assert repository.database == {species.id_: species,
                                       species2.id_: species2}
        assert repository.find(filters={"creator": "Tester"}) \
               == (2, [species, species2])

    def test_find_species_shouldnt_return_not_matches(self, repository):
        species = Species(creator="Tester")
        repository.create(species)
        species2 = Species(creator="Tester")
        repository.create(species2)
        species3 = Species(creator="Admin")
        repository.create(species3)
        assert repository.database == {species.id_: species,
                                       species2.id_: species2,
                                       species3.id_: species3}
        assert repository.find(filters={"creator": "Tester"}) \
               == (2, [species, species2])

    def test_find_species_should_return_length_matches(self, repository):
        species = Species(creator="Tester")
        repository.create(species)
        species2 = Species(creator="Tester")
        repository.create(species2)
        assert repository.database == {species.id_: species,
                                       species2.id_: species2}
        assert repository.find(length=1, filters={"creator": "Tester"}) \
               == (1, [species])

    def test_find_species_should_skip_offset_matches(self, repository):
        species = Species(creator="Tester")
        repository.create(species)
        species2 = Species(creator="Tester")
        repository.create(species2)
        assert repository.database == {species.id_: species,
                                       species2.id_: species2}
        assert repository.find(offset=1, filters={"creator": "Tester"}) \
               == (1, [species2])

    def test_delete_should_remove_from_database(self, repository):
        species = Species(creator="Tester")
        repository.create(species)
        assert repository.database == {species.id_: species}
        repository.delete(species.id_)
        assert repository.database == dict()

    @mark.parametrize("arg", [
        "1243",
        dict(),
        list(),
        True,
        None
    ])
    def test_update_with_non_species_arg_should_throw(self, repository, arg):
        with raises(NotEntityException):
            repository.update(arg)

    def test_update_should_raise_if_entity_not_found(self, repository):
        species = Species(creator="tester")
        with raises(EntityNotFoundException):
            repository.update(species)

    def test_update_should_update_entity(self, repository):
        species = Species(creator="tester")
        repository.create(species)
        species.scientific_name = "testum executum"
        assert repository.findOne({"creator": "tester",
                                   "scientific_name": "testum executum"}) \
               is None
        repository.update(species)
        assert repository.findOne({"creator": "tester",
                                   "scientific_name": "testum executum"}) \
               is not None
        species.popular_names = ["test"]
        assert repository.findOne({"creator": "tester",
                                   "scientific_name": "testum executum",
                                   "popular_names": ["test"]}) \
               is None
        repository.update(species)
        assert repository.findOne({"creator": "tester",
                                   "scientific_name": "testum executum",
                                   "popular_names": ["test"]}) \
               is not None

    def test_find_species_should_return_if_contains_popular_name(self,
                                                                 repository):
        species = Species(popular_names=["cagaita", "caganeira"])
        repository.create(species)
        assert repository.database == {species.id_: species}
        assert repository.find(filters={"popular_name": "cagaita"}) \
               == (1, [species])
        assert repository.find(filters={"popular_name": "cagait"}) \
               == (0, [])
