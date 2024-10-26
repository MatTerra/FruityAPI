from core.entity.favorites import Favorites
from core.usecase.species.unfavorite_species import UnfavoriteSpeciesInput, UnfavoriteSpecies
from infra.repository.favorite_memory_repository import FavoriteMemoryRepository
from test import container


class TestUnfavoriteSpecies:
    def test_shouldnt_accept_extra_args(self):
        test = {"extra": 1, "species": "a", "user": "a"}
        assert UnfavoriteSpeciesInput(**test).__dict__.get("extra") is None

    async def test_should_update_species_on_repository(self):
        repository = FavoriteMemoryRepository()
        with container.favorite.override(repository):
            favorite = Favorites(user="tester", species={"esp_1", "esp_2"}, trees={"tree_1", "tree_2"})
            repository.create(favorite)
            assert repository.find_by_user_id("tester") == favorite

            unfavorite_species = UnfavoriteSpecies()
            await unfavorite_species.execute(
                UnfavoriteSpeciesInput(user="tester",
                                     species="esp_2"))

            favorites = repository.find_by_user_id("tester")
            assert favorites is not None
            assert favorites.species == {"esp_1"}
            assert favorites.trees == {"tree_1", "tree_2"}
