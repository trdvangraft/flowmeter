import logging
from src.models.order import Order
from src.logger import root_logger
from src.blueprints import common_counter

from flask import (
    Blueprint, flash, g, request
)

logger = logging.getLogger(__name__)
logger.addHandler(root_logger.handlers[0])

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('', methods=['POST'])
@common_counter
def order():
    data = request.get_json()
    order = Order(**data)
    
    logger.info(f"Order received {request.data}")
    return {"order_id": order.id}, 201

@bp.route('/<order_id>', methods=['GET'])
@common_counter
def get_order(order_id):
    logger.info(f"Get order {order_id}")
    return "Order received", 200

@bp.route('/<order_id>/status', methods=['GET'])
@common_counter
def get_order_status(order_id):
    logger.info(f"Get order status {order_id}")
    return "Order status received", 200