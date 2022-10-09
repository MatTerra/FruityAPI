import os

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from core.repository.species_repository import SpeciesRepository
from infra.repository.species_memory_repository import SpeciesMemoryRepository
from infra.repository.species_sql_repository import SpeciesSQLRepository


class RepositoryContainer(DeclarativeContainer):
    config = providers.Configuration()

    species = providers.Singleton(
        SpeciesSQLRepository
        if os.getenv("TEST") != "1"
        else SpeciesMemoryRepository,
    )
