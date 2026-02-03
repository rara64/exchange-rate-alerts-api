from flask import Flask
from flask_restful import Api

from routes.base import Base
from routes.register import Register
from routes.login import Login
from routes.alerts import Alerts

from pymongo import MongoClient

app = Flask(__name__)
db : MongoClient = None

api = Api(app)

api.add_resource(Base, "/")
api.add_resource(Login, "/login", resource_class_args=(db,))
api.add_resource(Register, "/register", resource_class_args=(db,))
api.add_resource(Alerts, "/alerts", resource_class_args=(db,))

@app.errorhandler(404)
def not_found(e):
    return {'message': 'Requested resource was not found.'}, 404

if __name__ == "__main__":
    db = MongoClient()
    app.run()