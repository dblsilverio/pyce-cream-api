import logging

from sqlalchemy.orm import Session

from models.user import User as Entity


logger = logging.getLogger(__name__)


def find_user(db: Session, email: str):
    user = db.query(Entity).filter(Entity.email == email).one_or_none()

    if user is None:
        logger.info(f'User {email} not found')
        return None

    logger.info(f'User {email} found')

    return user
