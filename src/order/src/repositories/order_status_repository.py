from collections import defaultdict
from typing import Protocol, Optional, Any

from src.models import OrderStatus
from src.clients.redis_client import redis_client
from src.clients.mqtt_client import mqtt_client

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client as MqttClient
from redis import Redis

ORDER_STATUS_TOPIC = "order/status"

class ProtocolOrderStatusRepository(Protocol):
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage) -> None: ...
    
    def get(self, key: str) -> Optional[OrderStatus]: ...
    def set(self, key: str, value: OrderStatus) -> None: ...

class OrderStatusRepository(ProtocolOrderStatusRepository):
    def __init__(self, mqtt_client: MqttClient, redis_client: Redis) -> None:
        self.mqtt_client = mqtt_client
        self.redis_client = redis_client
        
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.subscribe(ORDER_STATUS_TOPIC)
        
    def get(self, key: str) -> Optional[OrderStatus]:
        order_status = self.redis_client.get(key)       
        return OrderStatus.model_validate_json(order_status) if order_status else None
    
    def set(self, key: str, value: OrderStatus) -> None:
        self.redis_client.set(key, value.serialize())
        
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage) -> None:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        
        if topic == ORDER_STATUS_TOPIC:
            self._handle_order_status(payload)
            
    def _handle_order_status(self, payload: str) -> None:
        order_status = OrderStatus(**payload)
        self.set(order_status.order_id, order_status)
        
class FakeOrderStatusRepository(ProtocolOrderStatusRepository):
    def __init__(self) -> None:
        self.order_status: dict[str, OrderStatus] = dict()
        
    def get(self, key: str) -> Optional[OrderStatus]:
        if key not in self.order_status:
            return None        
        return self.order_status.get(key)
    
    def set(self, key: str, value: OrderStatus) -> None:
        self.order_status[key] = value
        
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage) -> None:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        
        if topic == ORDER_STATUS_TOPIC:
            self._handle_order_status(payload)
    
    def _handle_order_status(self, payload: str) -> None:
        order_status = OrderStatus(**payload)
        self.set(order_status.order_id, order_status)
        
FAKE_ORDER_STATUS_REPOSITORY = FakeOrderStatusRepository()
ORDER_STATUS_REPOSITORY = OrderStatusRepository(
    mqtt_client=mqtt_client, redis_client=redis_client)
    