from sqlalchemy import Column, Integer, String, Float, Boolean

from infra.database import Base


class Flavor(Base):
    __tablename__ = 'flavors'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    available = Column(Boolean, nullable=False)
