from flask_restful import Resource, current_app
from modules.authentication import authenticated
from modules.exchange_rates import get_current_market_rate, RateProviderError, RateNotFoundError

class Alerts(Resource):
    def __init__(self, db):
        self.db = db
        self.col = db[current_app.config["TARGETS_COLLECTION"]]
    
    """
    /alerts GET

    RETURNS

    ...
    {
        "base_currency": str
        "exchange_currency": str
        "target_value": float
        "current_value": float
    }
    ...

    """
    @authenticated
    def get(self, user_id=""):
        user_targets = list(self.col.find({"user_id": user_id}, {"user_id": 0, "_id": 0}))
        alerts = list()

        for target in user_targets:
            try:
                current_rate = get_current_market_rate(target["base_currency"], target["quote_currency"])
            except (RateProviderError, RateNotFoundError):
                return {"message":"Service is temporarly unavailable due to rate provider error."}, 500
            
            if float(target["target_value"]) >= current_rate:
                new_alert = { **target, "current_value": current_rate}
                alerts.append(new_alert)

        return alerts, 200