from flask import Flask
from flask_restful import Api

from routes.register import Register
from routes.login import Login
from routes.alerts import Alerts
from routes.targets import Targets

from os import environ
from dotenv import load_dotenv
from uuid import uuid4
from pymongo import MongoClient

def create_app(config=None, mongo_client=None):
    load_dotenv()
    app = Flask(__name__)

    app.config.update(
        TOKEN_KEEPALIVE_MINUTES = environ.get("TOKEN_KEEPALIVE_MINUTES", 15),
        JWT_SECRET = environ.get("JWT_SECRET", str(uuid4())),
        MONGO_STR = environ.get("MONGO_STR", ""),
        USERS_COLLECTION = environ.get("USERS_COLLECTION", "users"),
        TARGETS_COLLECTION = environ.get("TARGETS_COLLECTION", "targets")
    )

    if config:
        app.config.update(config)

    if mongo_client:
        client = mongo_client
    else:
        client = MongoClient(app.config["MONGO_STR"])
    
    db = client["exchange_rates_alerts"]

    api = Api(app)

    api.add_resource(Login, "/login", resource_class_args=(db,))
    api.add_resource(Register, "/register", resource_class_args=(db,))
    api.add_resource(Alerts, "/alerts", resource_class_args=(db,))
    api.add_resource(Targets, "/targets", resource_class_args=(db,))

    @app.errorhandler(404)
    def not_found(e):
        return {'message': 'Requested resource was not found.'}, 404

    @app.route("/")
    def base():
        return {"message": "Everything is OK."}, 200
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()