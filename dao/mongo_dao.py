from typing import Dict, Any

from bson import ObjectId

from database.mongoDB import word_collection

async def insert_one(data : Dict[str, Any]):
    word_collection.insert_one(data)


async def get_by_id(mongo_id):
    document = word_collection.find_one({"_id": ObjectId(mongo_id)})
    return document