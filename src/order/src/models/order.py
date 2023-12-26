from typing import List
import uuid
from datetime import datetime

from src.models.order_item import OrderItem

from pydantic import BaseModel, Field

class QuantifiedOrderItem(BaseModel):
    quantity: int
    item: OrderItem
    
    def __eq__(self, other):
        return self.item == other.item
class Order(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    customer_id: str
    order_list: List[QuantifiedOrderItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def allocate(self, order_item):
        if order_item in self.order_list:
            index = self.order_list.index(order_item)
            self.order_list[index].quantity += order_item.quantity
        else:
            self.order_list.append(order_item)
    
    