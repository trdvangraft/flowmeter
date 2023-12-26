import logging
import os

from logger import root_logger

from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

from models.order import Order

logger = logging.getLogger(__name__)
logger.addHandler(root_logger.handlers[0])

app = Flask(__name__)
metrics = PrometheusMetrics(app, path=None)

PrometheusMetrics.init_app(app)



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    metrics.start_http_server(9600)
    app.run(debug=False, host='0.0.0.0', port=port)
    
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    
    return app
