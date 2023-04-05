"""
pydantic schemas definition for user
"""
from dataclasses import dataclass
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    """
    class to represent ObjectId because MongoDB stores data as BSON
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid Object Id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CurrencyType(Enum):
    """currency type definition"""
    CLP = "CLP"
    USD = "USD"
    EUR = "EUR"


class ItemSchema(BaseModel):
    """properties to define a item"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    category: str
    price: float
    currency: CurrencyType
    is_offer: bool | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "PS5",
                "category": "Video Games",
                "price": "550.000",
                "currency": "CLP",
                "is_offer": "True"
            }
        }


class ResponseSchema(BaseModel):
    """class to represent the services exception to return to  presentation layer"""
    detail: str
    data: dict | None = None


@dataclass
class ServiceException(Exception):
    """ class to represent the services exception to return to  presentation layer """
    detail: str
    status_code: int
