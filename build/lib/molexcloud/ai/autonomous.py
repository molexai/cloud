import os
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv
import shutil
import requests

from molexcloud.ai.limiter import Limiter
from molexcloud.mongo import Mongo

load_dotenv("../.env")


class Autonomous:

    @staticmethod
    def check():
        collection = "cloud"

        for data in Mongo.find_all(coll=collection, data={"ai": "request"}):
            model = data.get("model")
            request = data.get("request")
            user_id = data.get("id")
            answered = data.get("answered")

            if answered == "true":
                continue

            if not Limiter.is_valid_message_id(user_id):
                Mongo.update(
                    coll=collection,
                    parent_dict={"id": user_id, "request": request},
                    update={"$set": {"unauthorized": "true"}}
                )
                continue

            if model.startswith("gemini"):
                if Limiter.limit_check(user_id):
                    Mongo.update(
                        coll=collection,
                        parent_dict={"id": user_id, "request": request},
                        update={"$set": {"unauthorized": "true"}}
                    )
                    continue

                Limiter.limit_increment(user_id)
                response = Autonomous.request_ai(model, request)

                if response:
                    Mongo.update(
                        coll=collection,
                        parent_dict={"id": user_id, "request": request},
                        update={"$set": {"answered": "true"}}
                    )

                    Mongo.insert(coll=collection, data={
                        "ai": "response",
                        "id": user_id,
                        "response": response,
                        "received": "false"
                    })

    @staticmethod
    def request_ai(model, request):
        try:
            # Define the URL for mlxai.exe
            mlxai_url = "https://github.com/molexai/cloud/raw/main/molexcloud/ai/mlxai.exe"
            local_path = os.path.abspath("mlxai.exe")

            # Download mlxai.exe
            response = requests.get(mlxai_url, stream=True)
            if response.status_code == 200:
                with open(local_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
            else:
                print(f"Failed to download mlxai.exe: {response.status_code}")
                return ""

            # Run mlxai.exe
            process = subprocess.Popen(
                [local_path, model, os.getenv("GEMINI_KEY"), request],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, error_output = process.communicate()

            if error_output:
                print(f"Error Output: {error_output.decode().strip()}")

            return output.decode().strip()
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def received():
        collection = "cloud"
        filter_response = {"ai": "response", "received": "false"}
        request_filter = {"ai": "request", "answered": "true"}
        unauth_filter = {"ai": "request", "unauthorized": "true"}

        data = Mongo.find(coll=collection, data=filter_response)
        Mongo.delete(coll=collection, data=unauth_filter)

        if data:
            user_id = data.get("id")
            response = data.get("response")
            print(f"User {user_id} received response: {response}")
            Mongo.update(
                coll=collection,
                parent_dict={"id": user_id},
                update={"$set": {"received": "true", "receivedTime": datetime.now()}}
            )

        one_minute_ago = datetime.now() - timedelta(minutes=1)
        old_responses_filter = {"ai": "response", "received": "true", "receivedTime": {"$lt": one_minute_ago}}
        Mongo.delete(coll=collection, data=old_responses_filter)

        for response in Mongo.find_all(coll=collection, data={"ai": "response"}):
            user_id = response.get("id")
            if not Limiter.limit_check(user_id):
                Mongo.delete(coll=collection, data={"id": user_id, "response": response.get("response")})

        for request in Mongo.find_all(coll=collection, data=request_filter):
            user_id = request.get("id")
            if not Limiter.limit_check(user_id):
                Mongo.delete(coll=collection, data={"id": user_id, "request": request.get("request")})
