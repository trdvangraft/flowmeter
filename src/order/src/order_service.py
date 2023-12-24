import logging
import time
import os

from logger import root_logger
from mqtt_broker import MqttBroker

from prometheus_client import start_http_server

from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

logger = logging.getLogger(__name__)
logger.addHandler(root_logger.handlers[0])

app = Flask(__name__)
metrics = PrometheusMetrics(app, path=None)

common_counter = metrics.counter(
    name='by_endpoint_counter', description='Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)

@app.route('/order', methods=['POST'])
@common_counter
def order():
    logger.info(f"Order received {request.data}")
    return "Order received", 200

@app.route('/order/<order_id>', methods=['GET'])
@common_counter
def get_order(order_id):
    logger.info(f"Get order {order_id}")
    return "Order received", 200

@app.route('/order/<order_id>/status', methods=['GET'])
@common_counter
def get_order_status(order_id):
    logger.info(f"Get order status {order_id}")
    return "Order status received", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    metrics.start_http_server(9600)
    app.run(debug=False, host='0.0.0.0', port=port)


# def main():
#     logger.info("Order service started")
#     mqtt_broker = MqttBroker(client_id="order_service")
#     mqtt_broker.connect("mqtt", 1883, 60)
    
#     # Start up the server to expose the metrics.
#     start_http_server(9600)
    
#     topics = ["order_to_customer/#", "order_to_delivery/#", "delivery_to_order/#"]
#     for topic in topics:
#         mqtt_broker.subscribe(topic)
    
#     mqtt_broker.loop_start()
    
    
#     while True:
#         mqtt_broker.publish("order_to_customer", "Hello from order")
#         time.sleep(.2)
    
# if __name__ == '__main__':
#     main()