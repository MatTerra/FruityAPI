import os

from fastapi import FastAPI

from infra.repository.species_memory_repository import SpeciesMemoryRepository
from infra.routers.species_router import species_v1_router
from infra.repository import RepositoryContainer

repository_container = RepositoryContainer()
repository_container.wire(packages=["core", "infra"])
TEST = bool(os.getenv("TEST"))

app = FastAPI()


def start_api() -> FastAPI:
    api = FastAPI()
    api.container = repository_container
    api.include_router(species_v1_router)
    return api


if TEST:
    repository = SpeciesMemoryRepository()
    with repository_container.species.override(repository):
        print("Using memory database")
        app = start_api()
else:
    app = start_api()
