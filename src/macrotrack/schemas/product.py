from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    brand: str | None = Field(default=None, max_length=100)

    calories: Decimal = Field(ge=0, max_digits=8, decimal_places=2)
    protein: Decimal = Field(ge=0, max_digits=8, decimal_places=2)
    fat: Decimal = Field(ge=0, max_digits=8, decimal_places=2)
    carbs: Decimal = Field(ge=0, max_digits=8, decimal_places=2)


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    brand: str | None
    calories: Decimal
    protein: Decimal
    fat: Decimal
    carbs: Decimal
