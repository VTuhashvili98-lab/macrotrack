from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


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


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    brand: str | None = Field(default=None, max_length=100)

    calories: Decimal | None = Field(default=None, ge=0, max_digits=8, decimal_places=2)
    protein: Decimal | None = Field(default=None, ge=0, max_digits=8, decimal_places=2)
    fat: Decimal | None = Field(default=None, ge=0, max_digits=8, decimal_places=2)
    carbs: Decimal | None = Field(default=None, ge=0, max_digits=8, decimal_places=2)

    @model_validator(mode="after")
    def validate_null_values(self) -> Self:
        for field_name in ("name", "calories", "protein", "fat", "carbs"):
            if (
                field_name in self.model_fields_set
                and getattr(self, field_name) is None
            ):
                raise ValueError(f"{field_name} cannot be null")

        return self
