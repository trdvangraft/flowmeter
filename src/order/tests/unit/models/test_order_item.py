import pytest
from src.models import OrderItem, Pizza

def test_pizza_is_instance_of_order_item():
    pizza = Pizza(id="1234", name="pizza", toppings=["cheese"])
    assert isinstance(pizza, OrderItem)