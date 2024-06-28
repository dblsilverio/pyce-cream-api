from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from infra.database import get_db
from ucs.token.create_token import SECRET_KEY, ALGORITHM
from ucs.user.dtos import TokenData, User
from ucs.user.find_user import find_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """Grabs Bearer token Via OAuth2PasswordBearer and parse it to find an existing user.
    Fails if no user is found or token is invalid"""

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
    """Grabs the current active user only. If user is not active, it fails."""

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
