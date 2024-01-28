from pydantic import BaseModel, Field
from enum import Enum

class KitchenStatus(str, Enum):
    Open = "open"
    Closed = "closed"
    Maintenance = "maintenance"
    Unknown = "unknown"

class Kitchen(BaseModel):
    id: str
    name: str
    status: KitchenStatus = Field(default=KitchenStatus.Unknown)
    
    def serialize(self) -> str:
        return self.model_dump_json()
    
    def change_status(self, status: str):
        self.status = status
        
