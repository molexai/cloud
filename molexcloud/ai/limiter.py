import molexcloud.mongo

class Limiter:

    @staticmethod
    def limit_check(user_id):
        """Checks if the user has reached the limit"""
        data = molexcloud.mongo.Mongo.find(coll="molexcloud", data={"id": user_id})
        if data:
            limit = data["limit"]
            count = data["count"]
            if count >= limit:
                return True
        return False

    @staticmethod
    def limit_increment(user_id):
        """Increments the user's limit"""
        data = molexcloud.mongo.Mongo.find(coll="molexcloud", data={"id": user_id})
        if data:
            molexcloud.mongo.Mongo.update(coll="molexcloud", parent_dict={"id": user_id}, update={"$inc": {"count": 1}})

    @staticmethod
    def add_user(user_id, limit):
        """Adds a user to the database"""
        molexcloud.mongo.Mongo.insert(coll="molexcloud", data={"id": user_id, "limit": limit, "count": 0})

    @staticmethod
    def remove_user(user_id):
        """Removes a user from the database"""
        molexcloud.mongo.Mongo.delete(coll="molexcloud", data={"id": user_id})

    @staticmethod
    def get_user(user_id):
        """Gets a user from the database"""
        return molexcloud.mongo.Mongo.find(coll="molexcloud", data={"id": user_id})

    @staticmethod
    def reset_user(user_id):
        """Resets a user's count"""
        molexcloud.mongo.Mongo.update(coll="molexcloud", parent_dict={"id": user_id}, update={"$set": {"count": 0}})
