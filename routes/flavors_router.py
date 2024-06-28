import logging
from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from infra.caching_keys import function_kwargs_builder
from infra.database import get_db
from infra.security import get_current_active_user
from ucs.flavor.add_flavor import add_flavor
from ucs.flavor.dtos import Flavor
from ucs.flavor.list_flavors import get_flavor as get_flavor_from_db
from ucs.flavor.list_flavors import list_flavors
from ucs.user.dtos import User

router = APIRouter(
    prefix="/flavors",
    tags=["flavors"],
    responses={201: {"description": "Flavor created and available to use"},
               204: {"description": "No flavor available"},
               404: {"description": "Not found"},
               409: {"description": "Invalid flavor request"}},
)

logger = logging.getLogger(__name__)


@router.get("/", response_model=list[Flavor] | None)
@cache(expire=5, key_builder=function_kwargs_builder())
async def flavors(db: Session = Depends(get_db)):
    return list_flavors(db)

@router.get("/{flavor_id}")
@cache(expire=5, key_builder=function_kwargs_builder('flavor_id'))
async def get_flavor(flavor_id: int, db: Session = Depends(get_db)):
    flavor = get_flavor_from_db(db, flavor_id)

    if flavor is None:
        return JSONResponse({"message": f"Flavor id {flavor_id} not found"}, status_code=404)

    return flavor


@router.post("/")
async def new_flavor(flavor: Flavor,
                     current_user: Annotated[User, Depends(get_current_active_user)],
                     db: Session = Depends(get_db)):
    logger.info(f'User {current_user.email} is attempting to add a new flavor: {flavor.name}')
    added = add_flavor(db, flavor)

    if added is None:
        return JSONResponse(status_code=409, content={'message': f'Flavor {flavor.name} already exists'})

    return JSONResponse(status_code=201, content={}, headers={'Location': f'/flavors/{added.id}'})