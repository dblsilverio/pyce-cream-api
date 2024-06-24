import logging

from sqlalchemy.orm import Session

from infra import ice_repository
from ucs.dtos import Flavor, flavors


logger = logging.getLogger(__name__)


def add_flavor(db: Session, flavor: Flavor):
    logger.info(f'Adding flavor {flavor.name}')

    return ice_repository.add_flavor(db, flavor)
