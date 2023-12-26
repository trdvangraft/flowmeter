from typing import List

from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    id: str
    quantity: int

class Pizza(OrderItem):
    name: str
    toppings: List[str]
    extra_toppings: List[str] = Field(default_factory=list)
    removed_toppings: List[str] = Field(default_factory=list)