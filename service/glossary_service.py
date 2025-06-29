from model.glossary import GlossaryRequest
from dao import mongo_dao, pinecone_dao

async def upload_glossary(glossary_request: GlossaryRequest):
    """용어집 등록"""
    glossary_request_dict = glossary_request.to_dict()
    await mongo_dao.insert_one(glossary_request_dict)

def recommend(stt_data : str, k : int):
    recommend_glossary = pinecone_dao.query_stt(stt_data, k)
    return recommend_glossary