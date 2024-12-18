print("ABOUT TO START")
import os

import firebase_admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials

from infra.repository.species_sql_repository import SpeciesSQLDAO
from infra.repository.tree_sql_repository import TreeSQLDAO
from infra.routers.species_router import species_v1_router
from infra.routers.tree_router import tree_v1_router
from infra.routers.health_router import health_v1_router
from infra.repository import RepositoryContainer

print("IMPORT DONE")

repository_container = RepositoryContainer()
repository_container.wire(packages=["core", "infra"])

print("CREATED REPOSITORY CONTAINER")
TEST = bool(int(os.getenv("TEST", "0")))
if bool(int(os.getenv("CREATE_DB", "0"))):
    print("CREATE DB")
    dao = SpeciesSQLDAO()
    dao.create_table_if_not_exists()
    dao.close()
    dao = TreeSQLDAO()
    dao.create_table_if_not_exists()
    dao.close()
    print("CREATED DB")

print("STARTING FIREBASE")
cred = credentials.Certificate('/secrets/firebase_cred.json')
firebase_admin.initialize_app(cred)
print("STARTED FIREBASE")

print("STARTING APP")
app = FastAPI()
origins = ["http://localhost:57951",
           "https://fruity.matterra.com.br",
           "https://fruity.app.matterra.com.br"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.container = repository_container
app.include_router(species_v1_router)
app.include_router(tree_v1_router)
app.include_router(health_v1_router)
print("STARTED APP")
