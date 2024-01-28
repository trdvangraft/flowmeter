import pytest

from src.models import Order
from src.services import add_order_item, add_order_item, register_order
from src.repositories import FakeRedisRepository, FakeMqttRepository

def test_register_order():
    repo = FakeRedisRepository()
    order = Order(customer_id="1234")
    
    register_order(order, repo)
    
    assert repo.get(order.id) == order
