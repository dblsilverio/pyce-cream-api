import logging

from fastapi import FastAPI

import routes.flavors_router as flavors_router
import routes.users_router as users_router
from infra.database import Base, engine

# SQLAlchemy create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router.router)
app.include_router(flavors_router.router)

import infra.caching

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World"}

