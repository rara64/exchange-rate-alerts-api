from flask_restful import Resource, request, current_app
from modules.authentication import authenticated
from pymongo.database import Database
from modules.validator import is_valid_target_value, is_valid_currency_code

class Targets(Resource):
    def __init__(self, db : Database):
        self.db = db
        self.col = db[current_app.config["TARGETS_COLLECTION"]]
    
    """
    /targets GET
    """
    @authenticated
    def get(self, user_id=""):
        return list(self.col.find({"user_id": user_id}, {"user_id": 0, "_id": 0})), 200

    """
    /targets POST

    {
        "base_currency": str
        "quote_currency": str
        "target_value": float
    }
    """
    @authenticated
    def post(self, user_id=""):
        data = request.get_json()

        base_currency = data.get("base_currency")
        quote_currency = data.get("quote_currency")
        target_value = data.get("target_value")

        if None in (base_currency, quote_currency, target_value):
            return {"message":"One or more parameters are missing."}, 400
        
        if not is_valid_target_value(target_value):
            return {"message":"Target value is not in the correct format (#.####)."}, 400
        
        if not isinstance(base_currency, str) or not isinstance(quote_currency, str):
            return {"message": "base_currency and quote_currency must be strings."}, 400
        
        if is_valid_currency_code(base_currency) == False or is_valid_currency_code(quote_currency) == False:
            return {"message":"base_currency and quote_currency must be valid currency codes."}, 400

        query = {
                "base_currency": base_currency,
                "quote_currency": quote_currency,
                "user_id": user_id
        }

        self.col.update_one(query,
            { "$set" :
                {
                    "target_value": float(target_value)
                }
            }, upsert=True)

        insert_result = self.col.find_one(query, {"user_id": 0, "_id": 0})

        return insert_result, 201


    """
    /targets DELETE

    {
        "base_currency": str
        "quote_currency": str
    }
    """
    @authenticated
    def delete(self, user_id=""):
        data = request.get_json()

        base_currency = data.get("base_currency")
        quote_currency = data.get("quote_currency")

        if None in (base_currency, quote_currency):
            return {"message":"One or more parameters are missing."}, 400
        
        if not isinstance(base_currency, str) or not isinstance(quote_currency, str):
            return {"message": "base_currency and quote_currency must be strings."}, 400

        query = {
            "user_id": user_id,
            "base_currency": base_currency,
            "quote_currency": quote_currency
        }

        result = self.col.delete_one(query)

        if result.deleted_count > 0:
            return {"message": "Target removed successfully."}, 200
        else:
            return {"message": "Target not found."}, 404