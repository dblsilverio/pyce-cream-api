import logging
from typing import Annotated

import jwt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from infra import ice_repository
from infra.database import Base, engine, SessionLocal
from ucs.flavor.add_flavor import add_flavor
from ucs.flavor.dtos import Flavor
from ucs.flavor.list_flavors import list_flavors
from ucs.token.create_token import create_access_token, SECRET_KEY, ALGORITHM
from ucs.user.dtos import User, Token, TokenData
from ucs.user.find_user import find_user
from ucs.user.password_hash import verify_password

# SQLAlchemy create tables
Base.metadata.create_all(bind=engine)

#OAuth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except InvalidTokenError:
        raise credentials_exception
    user = find_user(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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
async def new_flavor(flavor: Flavor,
                     current_user: Annotated[User, Depends(get_current_active_user)],
                     db: Session = Depends(get_db)):
    logger.info(f'User {current_user.email} is attempting to add a new flavor: {flavor.name}')
    added = add_flavor(db, flavor)

    if added is None:
        return JSONResponse(status_code=409, content={'message': f'Flavor {flavor.name} already exists'})

    return JSONResponse(status_code=201, content={}, headers={'Location': f'/flavors/{added.id}'})


@app.post("/users/token")
async def login(user: User, db: Session = Depends(get_db)):
    logger.info(f'Login attempt by {user.email}')
    user_db = find_user(db, user.email)

    if user_db is None or not verify_password(user.password, user_db.hashed_password):
        logger.warning(f'Login failed for user {user.email}')
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({'sub': user_db.email})

    return Token(access_token=access_token,
                 token_type="bearer")

