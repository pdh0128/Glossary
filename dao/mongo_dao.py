from typing import Dict, Any
from database.mongoDB import word_collection

async def insert_one(data : Dict[str, Any]):
    word_collection.insert_one(data)
