import pytest

from src.models import Order, OrderItem, QuantifiedOrderItem
from src.repositories import RedisRepository

from pytest_redis import factories
from redis import Redis

redisdb_my_proc = factories.redis_proc()
redis_my = factories.redisdb(
    process_fixture_name="redisdb_my_proc",
    decode=True,
)

def test_redis_repository_can_save_order(redis_my: Redis):
    order = Order(customer_id="1234")
    repository = RedisRepository(redis_my)
    repository.set(order.id, order)

    assert Order.model_validate_json(redis_my.get(str(order.id))) == order
    
def test_redis_repository_can_get_order(redis_my: Redis):
    order = Order(customer_id="1234")
    repository = RedisRepository(redis_my)
    
    redis_my.set(str(order.id), order.serialize())

    assert repository.get(order.id) == order
    
def test_redis_repository_can_add_order(redis_my: Redis):
    order = Order(customer_id="1234")
    order.allocate(QuantifiedOrderItem(quantity=1, item=OrderItem(id="5678", name="calzone")))
    
    repository = RedisRepository(redis_my)
    
    repository.set(order.id, order)
    
    assert len(repository.get(order.id).order_list) == 1