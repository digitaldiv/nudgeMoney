from flask import Flask
from flask_restful import Api
from models import db, FinanceData, Stock, User, Portfolio
from schemas import ma, financeDataSchema, stockschema, userschema, portfolioschema
import logging
from flask_jwt_extended import JWTManager# , create_access_token, jwt_required, get_jwt_identity
import os
from routes import create_routes

# App initialization 
def create_app (test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    api = Api(app)  # API initialization 
    jwt = JWTManager(app)  # Authentication initialization 
    logging.basicConfig(filename='api.log', level=logging.DEBUG) # Logging initialization 
    db.init_app(app)   # Database initialization 
    ma.init_app(app) # Schema initialization

    create_routes(api)

    return app



"""    
    # HTML route
    @app.route('/')
    def index():
        return 'Hello APIs' 
"""

# ---------------------------
# Run app   
# ---------------------------
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8081)
