from flask_restful import Resource, current_app, request
from pymongo.database import Database
from modules.validator import is_valid_username, is_valid_password
import bcrypt

class Register(Resource):
    def __init__(self, db : Database):
        self.db = db
        self.col = db[current_app.config["USERS_COLLECTION"]]

    """
    /register POST

    {
        "username": string
        "password": string
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

        if is_valid_username(username) == False:
            return {"message":"Username is not in the correct format (3-20 characters, only letters and numbers)."}, 400
        
        if is_valid_password(password) == False:
            return {"message":"Password is not in the correct format (at least 8 characters, at least one letter and one number)."}, 400
        
        found_user = self.col.find_one({ "username": username })

        if found_user:
            return {"message": "User already exists."}, 409
        
        hashed_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

        self.col.insert_one({"username": username, "password": hashed_password})

        return {"message": "Registered successfully."}, 201