document = {
    "ai": "request",
    "id": "molexAI Administrator",
    "model": "gemini-1.5-flash",
    "request": "what is dark matter?"
}

from molexcloud.mongo import Mongo

Mongo.insert(coll="cloud", data=document)