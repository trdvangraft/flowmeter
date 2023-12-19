import logging

from paho.mqtt.client import Client as MqttClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.info(f"{msg.topic} {str(msg.payload)}")

    def loop_forever(self):
        self.client.loop_forever()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.disconnect()

def main():
    logging.info("Customer service started")
    
    mqtt_broker = MqttBroker(client_id="customer_service")
    mqtt_broker.connect("mqtt", 1883, 60)
    
    topics = ["order_to_customer/#", "customer_to_delivery/#", "delivery_to_customer/#"]
    for topic in topics:
        mqtt_broker.subscribe(topic)
    
    mqtt_broker.loop_forever()
    
if __name__ == '__main__':
    main()