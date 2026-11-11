from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from macrotrack.models.base import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("calories >= 0", name="ck_products_calories_nonnegative"),
        CheckConstraint("protein >= 0", name="ck_products_protein_nonnegative"),
        CheckConstraint("fat >= 0", name="ck_products_fat_nonnegative"),
        CheckConstraint("carbs >= 0", name="ck_products_carbs_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)

    calories: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    protein: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    fat: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    carbs: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
