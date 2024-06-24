import logging

from ucs.dtos import flavors


logger = logging.getLogger(__name__)


def list_flavors():
    logger.info('Listing flavors')
    return flavors
