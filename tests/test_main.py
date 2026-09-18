from fastapi.testclient import TestClient
from types import SimpleNamespace

from main import app
from utils.auth import get_current_user,require_admin


client = TestClient(app)


def fake_current_user():
    return SimpleNamespace(
        id=1,
        username="testuser",
        email="test@example.com",
        role="customer"
    )

def fake_admin_user():
    return SimpleNamespace(
        id=1,
        username="admin",
        email="admin@example.com",
        role="admin"
    )


app.dependency_overrides[get_current_user] = fake_current_user


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["message"] == "E-commerce API is running"


def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200


def test_get_cart():
    response = client.get("/cart/")

    assert response.status_code == 200


def test_add_to_cart():
    response = client.post(
        "/cart/add",
        params={
            "product_id": 1,
            "quantity": 2
        }
    )

    assert response.status_code == 200


def test_update_cart_quantity():
    response = client.put(
        "/cart/update/1",
        params={
            "quantity": 5
        }
    )

    assert response.status_code == 200


def test_remove_from_cart():
    response = client.delete("/cart/remove/1")

    assert response.status_code == 200


def test_create_order():
    add_response = client.post(
        "/cart/add",
        params={
            "product_id": 1,
            "quantity": 2
        }
    )

    assert add_response.status_code == 200

    order_response = client.post("/orders/")

    assert order_response.status_code == 200


def test_get_my_orders():
    response = client.get("/orders/")

    assert response.status_code == 200


def test_get_order():
    add_response = client.post(
        "/cart/add",
        params={
            "product_id": 1,
            "quantity": 2
        }
    )

    assert add_response.status_code == 200

    order_response = client.post("/orders/")

    assert order_response.status_code == 200

    order_id = order_response.json()["id"]

    response = client.get(
        f"/orders/{order_id}"
    )

    assert response.status_code == 200

def test_update_order_status():
    app.dependency_overrides[require_admin]=fake_admin_user

    add_response = client.post(
        "/cart/add",
        params={
            "product_id": 1,
            "quantity": 1
        }
    )

    assert add_response.status_code == 200

    order_response = client.post("/orders/")

    assert order_response.status_code == 200

    order_id = order_response.json()["id"]

    response = client.put(
        f"/orders/{order_id}/status",
        params={
            "status": "shipped"
        }
    )

    assert response.status_code == 200    

    app.dependency_overrides.pop(require_admin)

def test_get_all_orders_admin():
    app.dependency_overrides[require_admin]=fake_admin_user

    response=client.get("/orders/admin/all")

    assert response.status_code==200

    app.dependency_overrides.pop(require_admin)    

def test_unauthorized_access():
    app.dependency_overrides.pop(get_current_user)

    response = client.get("/products")

    assert response.status_code == 401

    app.dependency_overrides[get_current_user] = fake_current_user    

def test_customer_cannot_access_admin_orders():
    response=client.get("/orders/admin/all")

    assert response.status_code==403

def test_customer_cannot_update_order_status():
    response=client.put(
        "/orders/1/status",
        params={
            "status":"shipped"
        }
    )

    assert response.status_code==403

def test_order_not_found():
    response=client.get("/orders/999999")

    assert response.status_code==404    