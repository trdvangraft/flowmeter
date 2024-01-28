import logging
from src.models import Order, QuantifiedOrderItem, OrderStatus
from src.logger import root_logger
from src.blueprints import common_counter


import src.services as services
from src.repositories import RedisRepository, MqttRepository, OrderStatusRepository
from src.clients.redis_client import redis_client
from src.clients.mqtt_client import mqtt_client

from flask import (
    Blueprint, flash, g, request
)

logger = logging.getLogger(__name__)
logger.addHandler(root_logger.handlers[0])

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/create', methods=['POST'])
@common_counter
def order():
    # Write an arbitrary customer id to the order, as we do not have a customer service yet
    order = Order(customer_id="1234")
    order_status = OrderStatus(order_id=order.id)
    repo = RedisRepository(redis_client=redis_client)
    try :
        services.register_order(order, repo)
        services.register_order_status(order_status, repo)
    except Exception as e:
        logger.error(f"Error registering order {e}")
        return "Error registering order", 500
    
    logger.info(f"Order created {request.data}")
    return {"order_id": order.id}, 201

@bp.route('/<order_id>/add', methods=['POST'])
@common_counter
def add_order_item(order_id):
    repo = RedisRepository(redis_client=redis_client)
    qoi = QuantifiedOrderItem(**request.json)
    try:
        order_id = services.add_order_item(order_id=order_id, qoi=qoi, repository=repo)
    except Exception as e:
        logger.error(f"Error adding order item {e}")
        return "Error adding order item", 500
    
    logger.info(f"Order item added {request.data}")
    return {"order_id": order_id}, 201

@bp.route('/<order_id>/confirm', methods=['POST'])
@common_counter
def confirm_order(order_id):
    redis_repo = RedisRepository(redis_client=redis_client)
    mqtt_repo = MqttRepository(mqtt_client=mqtt_client)
    try:
        order_id = services.dispatch_order(order_id=order_id, redis_repository=redis_repo, mqtt_repository=mqtt_repo)
    except Exception as e:
        logger.error(f"Error confirming order {e}")
        return "Error confirming order", 500
    
    logger.info(f"Order confirmed {request.data}")
    return {"order_id": order_id}, 201

@bp.route('/<order_id>', methods=['GET'])
@common_counter
def get_order(order_id):
    logger.info(f"Get order {order_id}")
    return "Order received", 200

@bp.route('/<order_id>/status', methods=['GET'])
@common_counter
def get_order_status(order_id):
    order_status_repo = OrderStatusRepository(mqtt_client=mqtt_client, redis_client=redis_client)
    order_status = order_status_repo.get(order_id)
    return order_status, 200