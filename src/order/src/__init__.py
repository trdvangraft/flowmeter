from flask import Flask
from src.metrics import metrics

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
       
    metrics.init_app(app)
    
    with app.app_context():
        from .blueprints import order
        
        app.register_blueprint(order.bp)
        
        return app