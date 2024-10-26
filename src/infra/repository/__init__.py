import os

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from infra.repository.favorite_memory_repository import FavoriteMemoryRepository
from infra.repository.species_memory_repository import SpeciesMemoryRepository
from infra.repository.species_sql_repository import SpeciesSQLRepository
from infra.repository.tree_memory_repository import TreeMemoryRepository
from infra.repository.tree_sql_repository import TreeSQLRepository


class RepositoryContainer(DeclarativeContainer):
    config = providers.Configuration()

    species = providers.Singleton(
        SpeciesSQLRepository
        if os.getenv("TEST") != "1"
        else SpeciesMemoryRepository,
    )

    tree = providers.Singleton(
        TreeSQLRepository
        if os.getenv("TEST") != "1"
        else TreeMemoryRepository,
    )

    favorite = providers.Singleton(
        FavoriteMemoryRepository
        if os.getenv("TEST") != "1"
        else FavoriteMemoryRepository,
    )
