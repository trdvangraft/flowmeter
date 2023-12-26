from src.models import Order
from src.repositories import ProtocolRedisRepository

def register_order(order: Order, repository: ProtocolRedisRepository) -> None:
    repository.set(order.id, order)