from paho.mqtt.client import Client as MqttClient

class MqttBroker:
    def __init__(self, client_id: str):
        self.client = MqttClient(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self, host, port, keepalive):
        self.client.connect(host, port, keepalive)

    def on_connect(self, client: MqttClient, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"{msg.topic} {str(msg.payload)}")

    def loop_forever(self):
        self.client.loop_forever()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.disconnect()

def main():
    mqtt_broker = MqttBroker(client_id="order_service")
    print("hello")
    mqtt_broker.connect("mqtt", 1883, 60)
    
    topics = ["order_to_consumer/#", "order_to_delivery/#", "delivery_to_order/#"]
    for topic in topics:
        mqtt_broker.subscribe(topic)
    
    
    mqtt_broker.publish("order_to_consumer", "Hello from order")
    mqtt_broker.loop_forever()
    
if __name__ == '__main__':
    main()