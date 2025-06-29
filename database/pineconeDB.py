from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "glossary"
dimension = 1536

existing_indexes = [idx["name"] for idx in pc.list_indexes()]

spec = ServerlessSpec(
    cloud="aws",
    region="us-east-1",
)

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=spec
    )

index = pc.Index(index_name)

