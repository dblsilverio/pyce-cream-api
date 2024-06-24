import logging
from datetime import timedelta, datetime, timezone

import jwt

# Oauth JWT
SECRET_KEY = '8e8e092f6c6d48839b5b514b3edb7d57'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


logger = logging.getLogger(__name__)


def create_access_token(data: dict):
    logger.info(f'Creating access token for {data}')

    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)