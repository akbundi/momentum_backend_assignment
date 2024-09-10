# app/core/vector_db_service.py
import chromadb
from chromadb.config import Settings

class VectorDBService:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./vector_db"
        ))
        self.collection = self.client.get_or_create_collection("documents")

    def store_embeddings(self, embedding, metadata):
        asset_id = metadata.get("file_path")
        self.collection.add(
            ids=[asset_id],
            embeddings=[embedding.tolist()],
            metadatas=[metadata]
        )
        return asset_id

    def get_embedding(self, asset_id):
        results = self.collection.query(
            ids=[asset_id],
            n_results=1
        )
        return results["embeddings"][0] if results else None

    def asset_exists(self, asset_id):
        results = self.collection.query(ids=[asset_id], n_results=1)
        return bool(results["embeddings"])
