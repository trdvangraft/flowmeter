from unittest.mock import patch
import pytest

from src import init_app

@pytest.fixture
def app():
    app = init_app()
    app.config.update({
        "TESTING": True,
    })
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
    
    
def test_happy_order_creation(client):
    response = client.post('/order/create')
    
    assert response.status_code == 201
    assert "order_id" in response.json
    
    order_id = response.json["order_id"]
    json_data = {
        "item": {
            "id": "1234",
            "name": "Margherita",
            "toppings": ["cheese", "tomato"],
        },
        "quantity": 1
    }
    
    response = client.post(f'/order/{order_id}/add', json=json_data)
    
    assert response.status_code == 201
    assert "order_id" in response.json
    
    response = client.post(f'/order/{order_id}/confirm')
    
    assert response.status_code == 201
    assert "order_id" in response.json