from typing import Protocol
from pydantic import BaseModel, Field

class IceMachine(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    status: str
    max_capacity: int
    current_capacity: int
    ice_cream = Field(..., description="The amount of icecream in the machine")
    
    def assign(self) -> None:
        if self.current_capacity < self.max_capacity:
            self.current_capacity += 1
    
    def handle(self, item: IceCreamItem):
        # Check if the machine has enough icecream
        if self.ice_cream < item.size * 2:
            raise Exception("Not enough icecream")
        
        item.make()
        

        
    