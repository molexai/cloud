import os

from dotenv import load_dotenv

from mongo import Mongo
from limiter import Limiter

load_dotenv(".env")

class Autonomous:

    @staticmethod
    def check():
        """Checks for AI requests"""
        data = Mongo.find(coll="cloud", data={"ai": "request"})
        if data:
            model = data.get("model", None)
            request = data.get("request", None)
            user_id = data.get("id", None)
            answered = data.get("answered", "false")

            if answered == "true":
                return

            Mongo.update(coll="cloud", parent_dict={"ai": "request", "id": user_id}, update={"$set": {"answered": "true"}})

            if model.startswith("gemini"):
                limit = Limiter.limit_check(user_id)
                assert not limit, "User has reached the limit"
                Limiter.limit_increment(user_id)
                response = Autonomous.request(model, request)
                Mongo.insert(coll="cloud", data={"ai": "response", "id": user_id, "response": response, "received": "false"})


    @staticmethod
    def request(model, request):
        """Requests AI content"""
        response = os.system(f'{os.path.abspath("mlxai.exe")} "{model}" "{os.getenv("GEMINI_KEY")}" "{request}"')
        return str(response).replace("0", "").replace("\n", "").strip()

    @staticmethod
    def received():
        """Removes received AI responses"""
        data = Mongo.find(coll="cloud", data={"ai": "response", "received": "true"})
        if data:
            user_id = data["id"]
            response = data["response"]
            print(f"User {user_id} received response: {response}")
            Mongo.delete(coll="cloud", data={"ai": "response", "received": "true"})
            Mongo.delete(coll="cloud", data={"ai": "request", "id": user_id})
