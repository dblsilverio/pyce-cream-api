import logging

from fastapi import FastAPI

from ucs.add_flavor import add_flavor
from ucs.dtos import Flavor
from ucs.list_flavors import list_flavors

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/flavors")
async def flavors():
    return list_flavors()


@app.post("/flavors")
async def new_flavor(flavor: Flavor):
    add_flavor(flavor)
