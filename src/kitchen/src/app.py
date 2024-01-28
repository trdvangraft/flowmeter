
import multiprocessing as mp

from typing import Optional, Any
from models.order import Order

import services as services

from config import CONFIG

from clients.mqtt_client import MQTT_CLIENT

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client as MqttClient

import logging

import time


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ORDER_TOPIC = f"/orders/{CONFIG.KITCHEN_ID}"

class Kitchen:
    def __init__(self, client: MqttClient) -> None:
        self.client = client        
        self.client.on_message = self.on_message
        
        self.client.subscribe(ORDER_TOPIC)
    
    def start(self):
        self.client.loop_start()
    
    def on_message(self, 
                   client: MqttClient, 
                   userdata: Optional[Any], 
                   msg: mqtt.MQTTMessage) -> None:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        
        if topic == ORDER_TOPIC:
            self._handle_order_recieved(payload)
        else:
            raise Exception(f"Unknown topic {topic}")
            
    def _handle_order_recieved(self, payload: str) -> None:
        # Add your code here to handle the received message
        order = Order(**payload)
        services.put_order_to_queue(order, self.queue)
        services.get_approximate_time_to_delivery(order)
        
    
    def _handle_kitchen_discovery(self, payload: str) -> None:
        # Add your code here to handle the received message
        kitchen = Kitchen(**payload)
        self.kitchens.append(kitchen)
        
    
        
def start_order_process():
    logger.info("Starting order process")
    kitchen = Kitchen(MQTT_CLIENT)
    order_process = mp.Process(target=kitchen.start)
    return order_process

class Scheduler:
    def __init__(self) -> None:
        logger.info("Starting scheduler")
        
    def start(self):
        while True:
            time.sleep(5)
    
def main():
    order_process = start_order_process()
    # kitche_process = start_kitchen_process()
    
    sc = Scheduler()
    sc.start()
    
    
    
    
if __name__ == "__main__":
    main()