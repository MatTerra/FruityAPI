from core.entity.favorites import Favorites
from core.usecase.species.favorite_species import FavoriteSpecies, FavoriteSpeciesInput
from infra.repository.favorite_memory_repository import FavoriteMemoryRepository
from test import container


class TestFavoriteSpecies:
    def test_shouldnt_accept_extra_args(self):
        test = {"extra": 1, "species": "a", "user": "a"}
        assert FavoriteSpeciesInput(**test).__dict__.get("extra") is None

    async def test_should_update_species_on_repository(self):
        repository = FavoriteMemoryRepository()
        with container.favorite.override(repository):
            favorite = Favorites(user="tester", species={"esp_1", "esp_2"}, trees={"tree_1", "tree_2"})
            repository.create(favorite)
            assert repository.find_by_user_id("tester") == favorite

            favorite_species = FavoriteSpecies()
            await favorite_species.execute(
                FavoriteSpeciesInput(user="tester",
                                     species="esp_3"))

            favorites = repository.find_by_user_id("tester")
            assert favorites is not None
            assert favorites.species == {"esp_1", "esp_2", "esp_3"}
            assert favorites.trees == {"tree_1", "tree_2"}

    async def test_should_create_species_on_repository_if_doesnt_exist(self):
        repository = FavoriteMemoryRepository()
        with container.favorite.override(repository):
            assert repository.find_by_user_id("tester") is None

            favorite_species = FavoriteSpecies()
            await favorite_species.execute(
                FavoriteSpeciesInput(user="tester",
                                     species="esp_1"))

            favorites = repository.find_by_user_id("tester")
            assert favorites is not None
            assert favorites.species == {"esp_1"}
            assert favorites.trees == set()
