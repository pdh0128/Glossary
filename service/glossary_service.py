from core.fuzz_matching import fuzzy_match_words
from core.translator_gpt import ChatGPT
from model.glossary import GlossaryRequest, SttRequest
from dao import mongo_dao, pinecone_dao

async def upload_glossary(glossary_request: GlossaryRequest):
    """용어집 등록"""
    glossary_request_dict = glossary_request.to_dict()
    await mongo_dao.insert_one(glossary_request_dict)

def recommend(stt_data : str, k : int):
    recommend_glossary = pinecone_dao.query_stt(stt_data, k)
    return recommend_glossary

async def translate(stt_request : SttRequest):
    mongo_id = stt_request.mongo_id
    document = await mongo_dao.get_by_id(mongo_id)
    matched_word = await fuzzy_match_words(sentence=stt_request.text, word_list=document["word"], lang_field=stt_request.source_lang, threshold=50)
    chatgpt = ChatGPT()
    translated_text = await chatgpt.translate(sentence=stt_request.text, words=matched_word, resource_lang=stt_request.source_lang, target_lang=stt_request.target_lang)
    return translated_text