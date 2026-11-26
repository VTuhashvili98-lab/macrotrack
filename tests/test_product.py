from fastapi.testclient import TestClient


def test_delete_product_requires_admin(client: TestClient) -> None:
    response = client.delete("/products/1")

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid administrator credentials"}


def test_create_product_requires_admin(client: TestClient) -> None:
    response = client.post(
        "/products",
        json={
            "name": "Milk",
            "calories": 60,
            "protein": 3.2,
            "fat": 3.5,
            "carbs": 4.8,
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid administrator credentials"}


def test_update_product_requires_admin(client: TestClient) -> None:
    response = client.patch(
        "/products/1",
        json={"name": "Updated Milk"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid administrator credentials"}


def test_get_products(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexist_product(client: TestClient) -> None:
    response = client.get("products/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_get_product_invalid_id(client: TestClient) -> None:
    response = client.get("/products/-1")

    assert response.status_code == 422


def test_get_product_id_out_of_range(client: TestClient) -> None:
    response = client.get("/products/99999999999")

    assert response.status_code == 422
