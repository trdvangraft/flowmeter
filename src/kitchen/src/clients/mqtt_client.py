from paho.mqtt.client import Client as MqttClient

from config import CONFIG

import logging
import time

logger = logging.getLogger(__name__)

def connect() -> MqttClient:
    logger.info(f"Connecting to MQTT broker {CONFIG.MQTT_HOST}:{CONFIG.MQTT_PORT} client id: {CONFIG.MQTT_CLIENT_ID}")
    client = MqttClient(
       client_id=CONFIG.MQTT_CLIENT_ID,
    )
    
    while True:
        try:
            client.connect(
                host=CONFIG.MQTT_HOST,
                port=CONFIG.MQTT_PORT,
                keepalive=CONFIG.MQTT_KEEPALIVE,
            )
            break
        except Exception as e:
            logger.error(f"Error connecting to MQTT broker {e}")
            time.sleep(5)
    
    return client
    
MQTT_CLIENT = connect()


    