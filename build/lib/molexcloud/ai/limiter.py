import time

from molexcloud.mongo import Mongo

class Limiter:
    ONE_MINUTE_IN_MILLIS = 60000

    @staticmethod
    def is_valid_message_id(message_id):
        data = Mongo.find(coll="cloud", data={"message_id": message_id})
        return data is not None

    @staticmethod
    def limit_check(message_id):
        data = Mongo.find(coll="cloud", data={"message_id": message_id})
        if data:
            limit = data.get("limit")
            count = data.get("count")
            per_minute = data.get("per_minute")
            last_request_time = data.get("last_request_time")
            current_time = int(time.time() * 1000)

            if current_time - last_request_time >= Limiter.ONE_MINUTE_IN_MILLIS:
                Mongo.update(
                    coll="cloud",
                    parent_dict={"message_id": message_id},
                    update={"last_request_time": current_time}
                )
                Mongo.update(
                    coll="cloud",
                    parent_dict={"message_id": message_id},
                    update={"count": 0}
                )

            return count >= limit or count >= per_minute
        return False

    @staticmethod
    def limit_increment(message_id):
        current_time = int(time.time() * 1000)
        Mongo.update(
            coll="cloud",
            parent_dict={"message_id": message_id},
            update={"$inc": {"count": 1}, "$set": {"last_request_time": current_time}}
        )

    @staticmethod
    def add_user(message_id, limit, per_minute):
        current_time = int(time.time() * 1000)
        Mongo.insert(coll="cloud", data={
            "message_id": message_id,
            "limit": limit,
            "per_minute": per_minute,
            "count": 0,
            "last_request_time": current_time
        })

    @staticmethod
    def reset_user(message_id):
        current_time = int(time.time() * 1000)
        Mongo.update(
            coll="cloud",
            parent_dict={"message_id": message_id},
            update={"$set": {"count": 0, "last_request_time": current_time}}
        )
