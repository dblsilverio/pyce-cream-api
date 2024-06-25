import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from infra.database import get_db
from ucs.token.create_token import create_access_token
from ucs.user.create_user import create_user
from ucs.user.dtos import User, Token
from ucs.user.find_user import find_user
from ucs.user.password_hash import verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"description": "Invalid credentials"},
               404: {"description": "Not found"},
               409: {"description": "Invalid user creation request"}},
)


logger = logging.getLogger(__name__)


@router.post("/")
async def add_user(user: User, db: Session = Depends(get_db)):
    logger.info(f'Creating user {user.email}')

    user_created = create_user(user, db)

    if not user_created:
        return JSONResponse(status_code=409, content={'message': f'User {user.email} already exists'})

    return JSONResponse(status_code=201, content={})


@router.post("/token")
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