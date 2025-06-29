from typing import Dict, Any
from core.embeddings import chunk_words, embed
from database.pineconeDB import index as pinecone_index
from model.glossary import Glossary
from database.pineconeDB import index

def upsert(data : Dict[str, Any]):
    pinecone_index.upsert(data)

def insert_glossary(glossary : Glossary):
    for i, group in enumerate(chunk_words(glossary.word)):
        text_parts = []
        for word in group:
            text_parts.extend(word.values())
        combined_text = f"{glossary.title} {glossary.description} " + " ".join(text_parts)

        embedding = embed(combined_text)

        index.upsert([{
            "id": f"{glossary.mongo_id}-{i}",
            "values": embedding,
            "metadata": {
                "title": glossary.title,
                "description": glossary.description,
                "mongo_id": glossary.mongo_id,
                "chunk_index": i,
                "word_count": len(group)
            }
        }])


def delete_by_mongo_id(mongo_id : str):
    query_result = index.query(
        vector=[0.0] * 1536,
        filter={"mongo_id": mongo_id},
        top_k=1000,
        include_metadata=True
    )
    ids_to_delete = [match["id"] for match in query_result["matches"]]

    if ids_to_delete:
        index.delete(ids=ids_to_delete)
        print(f"{len(ids_to_delete)}개 벡터 삭제 완료")
    else:
        print("해당 mongo_id로 일치하는 벡터 없음")