import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def database_url(tmp_path):
    return f"sqlite:///{tmp_path / 'test.db'}"


@pytest.fixture
def client(database_url):
    with TestClient(create_app(database_url)) as test_client:
        yield test_client


@pytest.fixture
def payload():
    return {
        "amount": "12.50",
        "category": "Food",
        "description": "Fictional lunch",
        "expense_date": "2026-11-01",
    }


def test_create_expense(client, payload):
    response = client.post("/expenses", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result.items() >= payload.items()
    assert result["id"] > 0
    assert result["created_at"].endswith("Z")


def test_list_expenses(client, payload):
    assert client.get("/expenses").json() == []
    first = client.post("/expenses", json=payload).json()
    second = client.post("/expenses", json=payload).json()
    assert client.get("/expenses").json() == [first, second]
    assert client.get("/expenses?offset=1&limit=1").json() == [second]


def test_get_expense(client, payload):
    created = client.post("/expenses", json=payload).json()
    response = client.get(f"/expenses/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


@pytest.mark.parametrize("amount", ["0", "-1", "1.001", "NaN", "Infinity", "invalid", "10000000000.00", None])
def test_invalid_amount(client, payload, amount):
    payload["amount"] = amount
    assert client.post("/expenses", json=payload).status_code == 422
    assert client.get("/expenses").json() == []


@pytest.mark.parametrize("field,value", [("category", "  "), ("expense_date", "invalid"), ("description", "x" * 1001)])
def test_invalid_fields(client, payload, field, value):
    payload[field] = value
    assert client.post("/expenses", json=payload).status_code == 422


def test_nonexistent_expense(client):
    response = client.get("/expenses/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}


def test_persistence_across_app_restarts(database_url, payload):
    with TestClient(create_app(database_url)) as client:
        created = client.post("/expenses", json=payload).json()
    with TestClient(create_app(database_url)) as client:
        assert client.get(f"/expenses/{created['id']}").json() == created
