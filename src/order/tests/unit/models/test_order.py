import pytest

from src.models.order import Order
from src.models.order_item import OrderItem

def make_order_and_order_item():
    order = Order(customer_id="1234")
    order_item = OrderItem(id="1234", quantity=1)
    return order, order_item

def test_can_allocate_order_item_to_order():
    order, order_item = make_order_and_order_item()
    order.allocate(order_item)
    assert order.order_list == [order_item]
    
def test_can_increase_quantity_of_existing_order_item():
    order, order_item = make_order_and_order_item()
    order.allocate(order_item)
    order.allocate(order_item)
    assert order.order_list == [order_item]
    assert order.order_list[0].quantity == 2
    
def test_can_allocate_multiple_different_order_items():
    order, order_item = make_order_and_order_item()
    order.allocate(order_item)
    order.allocate(OrderItem(id="5678", quantity=1))
    assert len(order.order_list) == 2