from flask_restful import request, current_app
from functools import wraps
import jwt
from datetime import datetime, timezone, timedelta

def generate_token(user_id : str) -> str:
    keepalive = int(current_app.config["TOKEN_KEEPALIVE_MINUTES"])
    secret = current_app.config["JWT_SECRET"]

    payload = {
        "user_id": user_id,
        "expiry_date": str(datetime.now(timezone.utc) + timedelta(minutes=keepalive))
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        try:
            if not auth_header.startswith("Bearer "):
                raise Exception
        
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])

            if datetime.now(timezone.utc) > datetime.fromisoformat(payload["expiry_date"]):
                raise Exception
            
            if "user_id" not in payload:
                raise Exception 
            
            if not isinstance(payload["user_id"], str):
                raise Exception
        except:
            return {"message" : "Access unauthorized."}, 401

        return f(user_id=payload["user_id"], *args, **kwargs)
    return decorated