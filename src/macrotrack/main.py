from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from macrotrack.database import get_session
from macrotrack.models.product import Product
from macrotrack.schemas.product import ProductRead

app = FastAPI()


@app.get("/health")
def health_check(
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    session.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/products", response_model=list[ProductRead])
def get_products(
    session: Annotated[Session, Depends(get_session)],
) -> list[Product]:
    return list(session.scalars(select(Product)).all())


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Product:
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product
