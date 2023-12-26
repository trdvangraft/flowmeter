import pytest

from src.models import Order
from src.repositories import RedisRepository

def test_redis_repository_can_save_order(redisdb):
    order = Order(customer_id="1234")
    repository = RedisRepository(redisdb)
    repository.set(order.id, order)
    assert repository.get(order.id) == order