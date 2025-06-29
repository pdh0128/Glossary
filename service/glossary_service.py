from model.glossary import GlossaryRequest
from dao import mongo_dao

async def upload_glossary(glossary: GlossaryRequest):
    """용어집 등록"""
    glossary_dict = glossary.to_dict()
    await mongo_dao.insert_one(glossary_dict)

