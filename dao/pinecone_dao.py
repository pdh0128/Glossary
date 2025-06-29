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

def filter_best_by_mongo_id(results):
    best_map = {}
    for item in results:
        mongo_id = item["metadata"]["mongo_id"]
        score = item["score"]
        if mongo_id not in best_map or best_map[mongo_id]["score"] < score:
            best_map[mongo_id] = item
    return list(best_map.values())

def query_stt(stt_data, k):
    embedding = embed(stt_data)
    query_result = pinecone_index.query(
        vector=embedding,
        include_metadata=True,
        top_k=k,
    )

    results = []
    for match in query_result.matches:
        results.append({
            "id": match.id,
            "score": match.score,
            "metadata": match.metadata,
        })
    filtered_results = filter_best_by_mongo_id(results)
    return filtered_results
