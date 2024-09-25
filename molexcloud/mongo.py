import pymongo
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Mongo:
    """
    MongoDB manager

    Attributes:
        _client: the client
        _db: the database
        _coll: the collection
    """
    _client = pymongo.MongoClient(
        os.getenv("CLIENT"),
        tls=True,
        tlsAllowInvalidCertificates=True  # Only if you're using self-signed certificates
    )
    _db = _client.MolexAI
    _coll = _db.workspace  # the collection is workspace by default
    _collections = ["cloud"]

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
        Updates data in the database

        Args:
            coll (str): the collection to update the data in
            parent_dict (dict): the parent dictionary for finding the document
            update (dict): the update data, which should be passed as a dict with fields to update
        """
        cls._coll = cls._db[coll] if coll in cls._collections else cls._coll
        # Wrap the update dictionary in $set if it doesn't already contain MongoDB operators
        if not any(key.startswith("$") for key in update.keys()):
            update = {"$set": update}
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
        Finds a single document in the database

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

    @classmethod
    def find_all(cls, coll=None, *, data=None) -> list[dict]:
        """
        Finds all documents matching the criteria in the database

        Args:
            coll (str): the collection to find the data in
            data (dict): the data to match documents (default: None)
        Returns:
            list of matching documents
        """
        cls._coll = cls._db[coll] if coll in cls._collections else cls._coll
        find_data = data if data is not None else {}
        cursor = cls._coll.find(find_data)
        return list(cursor)

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
