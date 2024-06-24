from enum import Enum

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, EmailStr


class Type(Enum):
    diet = 'diet'
    traditional = 'traditional'


class Flavor(BaseModel):
    id: PositiveInt | None = Field(None, gt=0)
    name: str
    type: Type | None = Type.traditional
    description: str | None = None
    price: PositiveFloat = Field(..., gt=0.0)
    available: bool

    class Config:
        from_attributes = True


class User(BaseModel):
    id: PositiveInt = Field(..., gt=0)
    email: EmailStr | None = None
    hashed_password: str | None = None
    is_active: bool

# test flavors
flavors = [
        Flavor(
            name="Vanilla",
            type=Type.traditional,
            description="A classic vanilla flavour",
            price=1.5,
            available=True
        ),
        Flavor(
            name="Chocolate",
            type=Type.traditional,
            description="Rich and creamy chocolate flavour",
            price=2.0,
            available=True
        ),
        Flavor(
            name="Strawberry",
            type=Type.traditional,
            description="Sweet and fruity strawberry flavour",
            price=1.8,
            available=False
        ),
        Flavor(
            name="Mint",
            type=Type.traditional,
            description="Refreshing mint flavour",
            price=1.5,
            available=True
        ),
        Flavor(
            name="Caramel",
            type=Type.traditional,
            description="Sweet and smooth caramel flavour",
            price=2.5,
            available=False
        )
    ]