from collections import defaultdict
from typing import Protocol, Optional
import paho.mqtt.client as mqtt

from prometheus_client import Counter, Histogram

# Create a counter metric
MESSAGE_SENT = Counter(name='messages_sent', documentation='Number of messages sent', labelnames=['topic'])
MESSAGES_RECEIVED = Counter(name='messages_received', documentation='Number of messages received', labelnames=['topic'])

# App service metrics
REQUEST_TIME = Histogram('request_processing_seconds', 'Time spent processing request', ['method', 'endpoint'])

class ProtocolMqttRepository(Protocol):
    def publish(self, topic: str, payload: str) -> None: ...
    def subscribe(self, topic: str) -> None: ...
    def unsubscribe(self, topic: str) -> None: ...
    
class MqttRepository:
    def __init__(self, mqtt_client: mqtt.Client):
        self.mqtt_client = mqtt_client
    
    def publish(self, topic: str, payload: str) -> None:
        self.mqtt_client.publish(topic, payload)
    
    def subscribe(self, topic: str) -> None:
        self.mqtt_client.subscribe(topic)
    
    def unsubscribe(self, topic: str) -> None:
        self.mqtt_client.unsubscribe(topic)
        
class FakeMqttRepository:
    def __init__(self):
        self.messages = defaultdict(list)
        self.subscription = set()
    
    def publish(self, topic: str, payload: str) -> None:
        self.messages[topic] = payload
    
    def subscribe(self, topic: str) -> None:
        self.subscription.add(topic)
    
    def unsubscribe(self, topic: str) -> None:
        self.subscription.remove(topic)