import logging

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from infra import ice_repository
from infra.database import Base, engine, SessionLocal
from ucs.add_flavor import add_flavor
from ucs.dtos import Flavor
from ucs.list_flavors import list_flavors

Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/flavors/{flavor_id}")
async def get_flavor(flavor_id: int, db: Session = Depends(get_db)):
    flavor = ice_repository.get_flavor(db, flavor_id)

    if flavor is None:
        return JSONResponse({"message": f"Flavor id {flavor_id} not found"}, status_code=404)

    return flavor

@app.get("/flavors")
async def flavors(db: Session = Depends(get_db)):
    all_flavors = list_flavors(db)

    if len(all_flavors) == 0:
        return JSONResponse(status_code=204, content={})

    return all_flavors


@app.post("/flavors")
async def new_flavor(flavor: Flavor, db: Session = Depends(get_db)):
    added = add_flavor(db, flavor)

    if added is None:
        return JSONResponse(status_code=409, content={'message': f'Flavor {flavor.name} already exists'})

    return JSONResponse(status_code=201, content={}, headers={'Location': f'/flavors/{added.id}'})
