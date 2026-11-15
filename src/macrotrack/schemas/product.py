from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    brand: str | None
    calories: Decimal
    protein: Decimal
    fat: Decimal
    carbs: Decimal
