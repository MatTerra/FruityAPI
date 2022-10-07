from infra.repository import RepositoryContainer

container = RepositoryContainer()
container.wire(packages=["core"])