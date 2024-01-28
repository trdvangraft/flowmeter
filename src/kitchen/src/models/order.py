from typing import List
import uuid
from datetime import datetime

from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    id: str
    name: str

class Pizza(OrderItem):
    toppings: List[str]
    extra_toppings: List[str] = Field(default_factory=list)
    removed_toppings: List[str] = Field(default_factory=list)
    
class QuantifiedOrderItem(BaseModel):
    quantity: int
    item: OrderItem
    
    def __eq__(self, other):
        return self.item == other.item

class Order(BaseModel):
    id: uuid.UUID
    customer_id: str
    order_list: List[QuantifiedOrderItem]
    created_at: datetime
    recieved_at: datetime = Field(default_factory=datetime.now)
            
    def serialize(self) -> str:
        return self.model_dump_json()