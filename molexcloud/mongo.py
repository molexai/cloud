import pymongo
from dotenv import load_dotenv
import os

# TODO: Make sure the env file is in the correct directory
load_dotenv()


# Disclaimer: Remember to add the collections you want to use in the _collections list

class Mongo:
    """
    MongoDB manager

    Attributes:
        _client: the client
        _db: the database
        _coll: the collection
    """
    _client = pymongo.MongoClient(os.getenv("CLIENT"))
    _db = _client.MolexAI
    _coll = _db.workspace  # the collection is workspace by default
    _collections = ["molexcloud"]

    @classmethod
    def insert(cls, coll=None, *, data=None):
        """
        Inserts data into the database

        Args:
            coll (str): the collection to insert the data into
            data (dict): the data to insert
        """
        cls._coll = cls._db[coll] if coll in cls._collections else cls._coll
        cls._coll.insert_one(data)

    @classmethod
    def update(cls, coll=None, *, parent_dict=None, update=None):
        """
        Updates data into the database

        Args:
            coll (str): the collection to update the data into
            parent_dict (dict): the parent dictionary
            update (dict): the update data
        """
        cls._coll = cls._db[coll] if coll in cls._collections else cls._coll
        cls._coll.update_one(parent_dict, update)

    @classmethod
    def delete(cls, coll=None, *, data=None):
        """
        Deletes data from the database

        Args:
            coll (str): the collection to delete the data from
            data (dict): the data to delete
        """
        cls._coll = cls._db[coll] if coll in cls._collections else cls._coll
        delete_data = data if data is not None else {}
        cls._coll.delete_one(delete_data)

    @classmethod
    def find(cls, coll=None, *, item=None, data=None) -> dict:
        """
        Finds data in the database

        Args:
            coll (str): the collection to find the data in
            item (str): the item to find
            data (dict): the data to find
        """
        cls._coll = cls._db[coll] if coll in cls._collections else cls._coll
        find_data = data if data is not None else {}
        result = cls._coll.find_one(find_data)
        if result is None:
            print(f"No document found with data: {find_data}")
            return {}
        return result if item is None else result.get(item, None)

    def add(self, coll):
        """
        Adds a collection to the database

        Args:
            coll (str): the collection to add
        """
        self._db.create_collection(coll)
        self._collections.append(coll)

    def drop(self, coll):
        """
        Drops a collection from the database

        Args:
            coll (str): the collection to drop
        """
        self._db.drop_collection(coll)
        self._collections.remove(coll)

    def show(self) -> list[str]:
        """
        Shows all collections in the database
        """
        return self._db.list_collection_names()