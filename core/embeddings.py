from typing import List, Dict
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed(text: str, model="text-embedding-3-small") -> list[float]:
    response = openai.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding


def chunk_words(words: List[Dict[str, str]], chunk_size=100):
    for i in range(0, len(words), chunk_size):
        yield words[i:i+chunk_size]
