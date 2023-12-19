import logging
import time

from paho.mqtt.client import Client as MqttClient
from prometheus_client import start_http_server, Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a counter metric
messages_sent = Counter(name='messages_sent', documentation='Number of messages sent')
class MqttBroker:
    def __init__(self, client_id: str):
        self.client = MqttClient(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

    def connect(self, host, port, keepalive):
        self.client.connect(host, port, keepalive)

    def on_connect(self, client: MqttClient, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"{msg.topic} {str(msg.payload)}")
        
    def on_publish(self, client, userdata, mid):
        logging.info(f"Message {mid} sent")
        messages_sent.inc()

    def loop_forever(self):
        self.client.loop_forever()
        
    def loop_start(self):
        self.client.loop_start()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.disconnect()

def main():
    logging.info("Order service started")
    mqtt_broker = MqttBroker(client_id="order_service")
    mqtt_broker.connect("mqtt", 1883, 60)
    
    # Start up the server to expose the metrics.
    start_http_server(9600)
    
    topics = ["order_to_customer/#", "order_to_delivery/#", "delivery_to_order/#"]
    # for topic in topics:
    #     mqtt_broker.subscribe(topic)
    
    mqtt_broker.loop_start()
    
    
    while True:
        mqtt_broker.publish("order_to_customer", "Hello from order")
        time.sleep(.2)
    
if __name__ == '__main__':
    main()