import logging

from ucs.dtos import Flavor, flavors


logger = logging.getLogger(__name__)


def add_flavor(flavor: Flavor):
    logger.info(f'Adding flavor {flavor.name}')
    flavors.append(flavor)