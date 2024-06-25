import logging

from sqlalchemy.orm import Session

from models.user import User as Entity
from ucs.user.dtos import User as DTO
from ucs.user.password_hash import bcrypt_password

logger = logging.getLogger(__name__)


def create_user(user: DTO, db: Session) -> bool:
    exists = db.query(Entity).filter(Entity.email == user.email).one_or_none()

    if exists is not None:
        logger.warning("User already exists")
        return False

    new_user = Entity(email=user.email,
                      hashed_password=bcrypt_password(user.password),
                      is_active=True,
                      )

    db.add(new_user)
    db.commit()

    return True