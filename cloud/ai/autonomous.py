from cloud.mongo import Mongo


class Autonomous:
    def check(self):
        """Checks for AI requests"""
        data = Mongo.find(coll="cloud", data={"ai": "request"})
        if data:
            model = data["model"]
            request = data["request"]
            id = data["id"]

            if model.startswith("gemini"):
                ...

        else:
            print("No AI requests found")