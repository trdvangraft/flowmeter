from paho.mqtt.client import Client as MqttClient

mqtt_client = None

def init_mqtt(app):
    global mqtt_client
    mqtt_client = MqttClient(
        client_id=app.config['MQTT_CLIENT_ID']
    )
    

# class MqttBroker:
#     def __init__(self, client_id: str):
#         self.client = MqttClient(client_id=client_id)
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.client.on_publish = self.on_publish

#     def connect(self, host, port, keepalive):
#         self.client.connect(host, port, keepalive)

#     def on_connect(self, client: MqttClient, userdata, flags, rc):
#         print(f"Connected with result code {rc}")

#     def on_message(self, client, userdata, msg):
#         logger.info(f"Message received on topic {msg.topic} with payload {msg.payload}")
#         MESSAGES_RECIEVED.labels(topic=msg.topic).inc()
        
#     def on_publish(self, client, userdata, mid):
#         logger.info(f"Message {mid} {userdata} {client} sent")

#     def loop_forever(self):
#         self.client.loop_forever()
        
#     def loop_start(self):
#         self.client.loop_start()

#     def subscribe(self, topic):
#         self.client.subscribe(topic)

#     def publish(self, topic, payload):
#         self.client.publish(topic, payload)
#         MESSAGE_SENT.labels(topic=topic).inc()

#     def disconnect(self):
#         self.client.disconnect()
