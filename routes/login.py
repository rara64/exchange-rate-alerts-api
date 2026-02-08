from flask_restful import Resource, current_app, request
from pymongo.database import Database
from modules.authentication import generate_token
import bcrypt

class Login(Resource):
    def __init__(self, db : Database):
        self.db = db
        self.col = db[current_app.config["USERS_COLLECTION"]]

    """
    /login POST

    {
        "username": string
        "password": string
    }

    RETURNS

    {
        "token": string
    }
    """
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if None in (username, password):
            return {"message":"One or more parameters are missing."}, 400
        
        if not isinstance(username, str) or not isinstance(password, str):
            return {"message": "Username and password must be strings."}, 400

        username = username.strip()

        found_user = self.col.find_one({ "username": username })

        if found_user:
            hashed_password = found_user.get("password")
            if bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password):
                token = generate_token(str(found_user.get("_id")))
                return { "token": token }, 200

        return {"message": "User or password is wrong."}, 401