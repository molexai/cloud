import os

from dotenv import load_dotenv

from molexcloud.mongo import Mongo
from molexcloud.ai.limiter import Limiter

load_dotenv("../.env")

class Autonomous:

    @staticmethod
    def check():
        """Checks for AI requests"""
        data = Mongo.find(coll="molexcloud", data={"ai": "request"})
        if data:
            model = data["model"]
            request = data["request"]
            user_id = data["id"]

            if model.startswith("gemini"):
                limit = Limiter.limit_check(user_id)
                assert not limit, "User has reached the limit"
                Limiter.limit_increment(user_id)
                response = Autonomous.request(model, request)
                Mongo.insert(coll="molexcloud", data={"ai": "response", "id": user_id, "response": response, "received": "false"})


    @staticmethod
    def request(model, request):
        """Requests AI content"""
        os.chdir("../..")
        response = os.system(f'mlxai.exe "{model}" "{os.getenv("GEMINI_KEY")}" "{request}"')
        os.chdir("molexcloud/ai")
        return str(response).replace("0", "").replace("\n", "").strip()

    @staticmethod
    def received():
        """Removes received AI responses"""
        data = Mongo.find(coll="molexcloud", data={"ai": "response", "received": "true"})
        if data:
            user_id = data["id"]
            response = data["response"]
            print(f"User {user_id} received response: {response}")
            Mongo.delete(coll="molexcloud", data={"ai": "response", "received": "true"})
            Mongo.delete(coll="molexcloud", data={"ai": "request", "id": user_id})
