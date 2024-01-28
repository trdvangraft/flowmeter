ORDER_TOPIC = f"/orders/{kitchen_id}"

class ProtocolOrderRepository(Protocol):
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage) -> None: ...
    
class OrderRepository(ProtocolOrderRepository):
    def __init__(self, client: MqttClient) -> None:
        self.client = client
        self.client.on_message = self.on_message
        self.client.subscribe(ORDER_STATUS_TOPIC)
        
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage) -> None:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        
        if topic == ORDER_STATUS_TOPIC:
            self._handle_order_status(payload)
            
    def _handle_order_status(self, payload: str) -> None:
        # Add your code here to handle the received message
        pass