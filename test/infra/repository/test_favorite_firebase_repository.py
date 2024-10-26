from firebase_admin import initialize_app, credentials, firestore
from pytest import fixture

from core.entity.favorites import Favorites
from infra.repository.favorite_firebase_repository import FavoriteFirebaseRepository


class TestFavoriteFirebaseRepository:
    @fixture(scope="session", autouse=True)
    def init_firebase(self):
        cred = credentials.Certificate('/secrets/firebase_cred.json')
        app = initialize_app(credential=cred)

    @fixture
    def repository(self):
        return FavoriteFirebaseRepository()

    def test_can_get_existant_favorite(self, repository):
        favorite = Favorites(user="tester", species={"esp_1"}, trees={"tree_1"})
        repository.create(favorite)
        assert repository.find_by_user_id("tester") == favorite
        repository.delete(favorite)

    def test_can_get_non_existant_favorite(self, repository):
        favorites = repository.find_by_user_id("teste_nao_existe")
        assert favorites is None


    def test_should_register_favorite_on_repository(self, repository):
        favorite = Favorites(user="tester", species={"esp_1", "esp_2"}, trees={"tree_1", "tree_2"})
        assert repository.create(favorite) == "tester"
        assert repository.find_by_user_id("tester") == favorite
        repository.delete(favorite)

    def test_should_update_favorite_on_repository(self, repository):
        favorite = Favorites(user="tester", species={"esp_1", "esp_2"}, trees={"tree_1", "tree_2"})
        assert repository.create(favorite) == "tester"
        assert repository.find_by_user_id("tester") == favorite

        favorite = Favorites(user="tester", species={"esp_3", "esp_4"}, trees={"tree_3", "tree_4"})
        assert repository.update(favorite) == "tester"
        assert repository.find_by_user_id("tester") == favorite

        repository.delete(favorite)

    def test_should_delete_favorite_on_repository(self, repository):
        favorite = Favorites(user="tester", species={"esp_1", "esp_2"}, trees={"tree_1", "tree_2"})
        assert repository.create(favorite) == "tester"
        assert repository.find_by_user_id("tester") == favorite
        repository.delete(favorite)
        assert repository.find_by_user_id("tester") is None

