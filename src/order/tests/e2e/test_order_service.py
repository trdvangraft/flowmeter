from unittest.mock import patch
import pytest
import uuid

from tests.utils import is_valid_uuid
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

def test_order_with_one_pizza(client):    
    json_data = {
        "customer_id": "1234",
        "order_list": [
            {
                "item": {
                    "id": "1234",
                    "name": "Margherita",
                    "toppings": ["cheese", "tomato"],
                },
                "quantity": 1
            }
        ]
    }
        
    response = client.post('/order', json=json_data)
    assert response.status_code == 201
    assert "order_id" in response.json
    assert is_valid_uuid(response.json["order_id"])
    
def test_order_creation(client):
    response = client.post('/order/create')
    assert response.status_code == 201
    assert "order_id" in response.json
    assert is_valid_uuid(response.json["order_id"])

def test_add_pizza_to_order(client):
    pass

def test_remove_pizza_from_order(client):
    pass

def test_comfirm_order(client):
    pass