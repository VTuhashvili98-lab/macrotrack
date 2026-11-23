from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from macrotrack.auth import require_admin
from macrotrack.database import get_session
from macrotrack.models.product import Product
from macrotrack.schemas.product import ProductCreate, ProductRead, ProductUpdate

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


@app.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_product(
    data: ProductCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Product:
    product = Product(**data.model_dump())

    session.add(product)

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()

        constraint_name = getattr(
            getattr(exc.orig, "diag", None),
            "constraint_name",
            None,
        )

        if constraint_name == "uq_products_name":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists",
            ) from exc

        raise

    session.refresh(product)

    return product


@app.patch(
    "/products/{product_id}",
    response_model=ProductRead,
    dependencies=[Depends(require_admin)],
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Product:
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    for field_name, value in update_data.items():
        setattr(product, field_name, value)

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()

        constraint_name = getattr(
            getattr(exc.orig, "diag", None),
            "constraint_name",
            None,
        )

        if constraint_name == "uq_products_name":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists",
            ) from exc

        raise

    session.refresh(product)

    return product


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_product(
    product_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> None:
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    session.delete(product)
    session.commit()
