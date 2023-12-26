from typing import Optional, Protocol

from src.models import Order

from redis import Redis

class ProtocolRedisRepository(Protocol):
    def get(self, key: str) -> Optional[Order]: ...
    def set(self, key: str, value: Order) -> None: ...
    
    

class RedisRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
    
    def get(self, key: str) -> Optional[Order]:
        order = self.redis_client.get(str(key))       
        return Order.model_validate_json(order) if order else None
    
    def set(self, key: str, value: Order) -> None:
        self.redis_client.set(str(key), value.serialize())

class FakeRedisRepository:
    def __init__(self):
        self.orders = {}
    
    def get(self, key: str) -> Optional[Order]:
        order = self.orders.get(key)
        return order
    
    def set(self, key: str, value: Order) -> None:
        self.orders[key] = value
    
