from flask import request
from src.metrics import metrics

common_counter = metrics.counter(
    name='by_endpoint_counter', description='Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)