import logging

from sqlalchemy.orm import Session

from infra import ice_repository

logger = logging.getLogger(__name__)


def get_flavor(db: Session, flavor_id: int):
    logger.info(f'Fetching flavor: {flavor_id}')
    return ice_repository.get_flavor(db, flavor_id)


def list_flavors(db: Session):
    logger.info('Listing flavors')
    return ice_repository.get_flavors(db)
