import logging

from sqlalchemy.orm import Session

from models.flavor import Flavor as Entity, Flavor
from ucs.dtos import Flavor as DTO


logger = logging.getLogger(__name__)


def get_flavors(db: Session):
    flavors = []

    entities = db.query(Entity).all()

    if entities and len(entities) > 0:
        flavors = [DTO.from_orm(entity) for entity in entities]

    return flavors


def add_flavor(db: Session, flavor: DTO) -> Flavor | None:
    logger.info(f'Adding flavor {flavor.name}')

    exists = db.query(Entity).filter(Entity.name == flavor.name).one_or_none()

    if exists is not None:
        logger.warning(f'Flavor {flavor.name} already exists')
        return None

    entity = Entity(name=flavor.name,
                    description=flavor.description,
                    price=flavor.price,
                    available=flavor.available,
                    type=flavor.type.name)
    db.add(entity)
    db.commit()

    logger.info(f'Flavor {flavor.name} added')

    return entity


def get_flavor(db, flavor_id):
    flavor = db.query(Flavor).filter(Flavor.id == flavor_id).first()

    if flavor is None:
        logger.warning(f'Flavor id {flavor_id} does not exist')
        return None

    return flavor