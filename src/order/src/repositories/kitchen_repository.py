from collections import defaultdict
from typing import Protocol, Optional, Any
from order.src.models import Kitchen

from src.models import Kitchen, Order
from src.clients.mqtt_client import mqtt_client

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client as MqttClient

KITCHEN_STATUS_TOPIC = "kitchen/status"
KITCHEN_DISCOVERY_TOPIC = "kitchen/discovery"

class ProtocolKitchenRepository(Protocol):
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage) -> None: ...
    def send_order_to_kitchen(self, order: Order, kitchen: Kitchen) -> None: ...
    def get_available_kitchen(self) -> Kitchen: ...
    
class KitchenRepository(ProtocolKitchenRepository):
    def __init__(self, client: MqttClient) -> None:
        self.client = client
        self.kitchens: list[Kitchen] = []
        
        self.client.on_message = self.on_message
        self.client.subscribe(KITCHEN_STATUS_TOPIC)
        self.client.subscribe(KITCHEN_DISCOVERY_TOPIC)
        
    def send_order_to_kitchen(self, order: Order, kitchen: Kitchen) -> None:
        self.client.publish(f"/orders/{kitchen.id}", order.model_dump_json())
        
    def get_available_kitchen(self) -> Kitchen:
        return self.kitchens[0]
    
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage) -> None:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        
        if topic == KITCHEN_STATUS_TOPIC:
            self._handle_kitchen_status(payload)
        elif topic == KITCHEN_DISCOVERY_TOPIC:
            self._handle_kitchen_discovery(payload)
            
    def _handle_kitchen_status(self, payload: str) -> None:
        # Add your code here to handle the received message
        pass
    
    def _handle_kitchen_discovery(self, payload: str) -> None:
        # Add your code here to handle the received message
        kitchen = Kitchen(**payload)
        self.kitchens.append(kitchen)
    
class FakeKitchenRepository(ProtocolKitchenRepository):
    def __init__(self) -> None:
        self.kitchens: list[Kitchen] = []
        self.send_messages: dict[str, list[Order]] = defaultdict(list)
        
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage
                ) -> None:
        
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        
        if topic == KITCHEN_STATUS_TOPIC:
            raise NotImplementedError()
        elif topic == KITCHEN_DISCOVERY_TOPIC:
            kitchen = Kitchen(**payload)
            self.kitchens.append(kitchen)
    
    def send_order_to_kitchen(self, order: Order, kitchen: Kitchen) -> None:
        # Add your code here to handle the received message
        self.send_messages[kitchen.id].append(order)
    
    def get_available_kitchen(self) -> Kitchen:
        return self.kitchens[0]
    
KITCHEN_REPOSITORY = KitchenRepository(mqtt_client=mqtt_client)
FAKE_KITCHEN_REPOSITORY = FakeKitchenRepository()
    