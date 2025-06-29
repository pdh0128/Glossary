from dao.mongo_dao import word_collection
from threading import Thread
from model.glossary import Glossary
from dao import pinecone_dao


def watch_word_collection():
    """
    mongo change stream
    MongoDB 레플리카 셋으로 설장해놔야 정상 작동하니깐 주의
    """
    with word_collection.watch() as stream:
        for change in stream:
            print("변경 감지됨:", change)
            if change["operationType"] == "insert":
                document = change["fullDocument"]
                glossary = glossary_factory(document)
                log_document_glossary(glossary)
                pinecone_dao.insert_glossary(glossary)
            elif change["operationType"] == "delete":
                mongo_id = str(change["documentKey"]["_id"])
                pinecone_dao.delete_by_mongo_id(mongo_id)

def glossary_factory(document):
    """용어집 생성"""
    mongo_id = str(document.get("_id"))
    title = document.get("title")
    description = document.get("description")
    words = document.get("word", [])
    glossary = Glossary(mongo_id=mongo_id, title=title, description=description, word=words)
    return glossary


def log_document_glossary(glossary : Glossary):
    """용어집 로그 찍기"""
    print(glossary.mongo_id)
    print(glossary.title)
    print(glossary.description)
    for word_set in glossary.word:
        for k, v in word_set.items():
            print(k + " " + v)


def start_change_stream_in_thread():
    thread = Thread(target=watch_word_collection, daemon=True)
    thread.start()
