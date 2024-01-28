import time

from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    size: int
    
    def make(self) -> None:
        raise NotImplementedError()
    
    
class IceCreamItem(Item):
    def make(self) -> None:
        print(f"Making {self.size} icecream")
        time.sleep(1)

class PizzaItem(Item):
    toppings: list[str]
    extra_toppings: list[str] = Field(default_factory=list)
    remove_toppings: list[str] = Field(default_factory=list)
    
    def make(self) -> None:
        _toppings = self.toppings + self.extra_toppings - self.remove_toppings
        
        print(f"Making {self.size} {self.name} with toppings: {_toppings}")