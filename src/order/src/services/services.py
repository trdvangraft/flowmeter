from src.models import Order, QuantifiedOrderItem, OrderItem, OrderStatus, OrderStatusEnum
from src.repositories import ProtocolRedisRepository, ProtocolKitchenRepository, ProtocolOrderStatusRepository

class OrderNotFound(Exception):
    pass

def register_order(order: Order, 
                   order_repository: ProtocolRedisRepository, 
                ) -> None:
    order_repository.set(order.id, order)
    
def register_order_status(order_status: OrderStatus, 
                          order_status_repository: ProtocolOrderStatusRepository
                          ) -> None:
    order_status_repository.set(order_status.order_id, order_status)
    
def add_order_item(
    order_id: str, 
    qoi: QuantifiedOrderItem, 
    order_repo: ProtocolRedisRepository,
    order_status_repo: ProtocolOrderStatusRepository
    ):
    order = order_repo.get(order_id)
    order_status = order_status_repo.get(order_id)
    
    if not order or not order_status:
        raise OrderNotFound(f"Order {order_id} not found")
    
    order.allocate(qoi)
    
    if order_status.status != OrderStatusEnum.Started:
        order_status.change_status(OrderStatusEnum.Started)
        order_status_repo.set(order_status.order_id, order_status)
    
    order_repo.set(order.id, order)
    return order.id

def dispatch_order(
    order_id: str,
    order_repo: ProtocolRedisRepository, 
    kitchen_repo: ProtocolKitchenRepository, 
    order_status_repo: ProtocolOrderStatusRepository
):
    order = order_repo.get(order_id)
    order_status = order_status_repo.get(order_id)
    kitchen = kitchen_repo.get_available_kitchen()
    
    if not order or not order_status:
        raise OrderNotFound(f"Order {order_id} not found")
    
    kitchen_repo.send_order_to_kitchen(order, kitchen)
    order_status.change_status(OrderStatusEnum.SentToKitchen)
    order_status_repo.set(order.id, order_status)
    
    return order.id