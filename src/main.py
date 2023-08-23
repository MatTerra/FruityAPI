import os

import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials

from infra.repository.species_sql_repository import SpeciesSQLDAO
from infra.routers.species_router import species_v1_router
from infra.repository import RepositoryContainer

repository_container = RepositoryContainer()
repository_container.wire(packages=["core", "infra"])
TEST = bool(os.getenv("TEST"))
if(bool(os.getenv("CREATE_DB"))):
    SpeciesSQLDAO().create_table_if_not_exists()

cred = credentials.Certificate('firebase_cred.json')
firebase_admin.initialize_app(cred)


app = FastAPI()
app.container = repository_container
app.include_router(species_v1_router)
