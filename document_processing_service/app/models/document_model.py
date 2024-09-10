# document_model.py

import uuid
import os
from typing import List
from gensim.models import KeyedVectors
import chromadb

class DocumentModel:
    def __init__(self, vector_db_directory: str = "./vector_db", word2vec_model_path: str = "./models/word2vec/word2vec_weights.bin"):
        # Initialize ChromaDB for vector storage
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=vector_db_directory
        ))
        self.collection = self.client.create_collection("documents")

        # Load Word2Vec model
        self.word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
        
    def process_document(self, file_path: str) -> str:
        # Generate a unique Asset ID for the document
        asset_id = str(uuid.uuid4())
        
        # Read file content
        file_content = self._read_file(file_path)
        
        # Create embeddings using Word2Vec
        embeddings = self._create_embeddings(file_content)
        
        # Store embeddings in the vector database
        self._store_embeddings(asset_id, embeddings, file_path)
        
        return asset_id
    
    def _read_file(self, file_path: str) -> str:
        """Reads content from a text, PDF, or Word file."""
        ext = os.path.splitext(file_path)[1]
        
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            # Implement PDF reading logic
            return "PDF content..."
        elif ext == '.doc' or ext == '.docx':
            # Implement Word reading logic
            return "Word content..."
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _create_embeddings(self, content: str) -> List[float]:
        """Create word embeddings from document content."""
        # Tokenize content into words
        tokens = content.split()

        # For simplicity, we'll average the embeddings of all words in the document
        embeddings = [self.word2vec_model[word] for word in tokens if word in self.word2vec_model]
        avg_embedding = sum(embeddings) / len(embeddings) if embeddings else []
        
        return avg_embedding

    def _store_embeddings(self, asset_id: str, embeddings: List[float], file_path: str):
        """Store the embeddings in the vector database with metadata."""
        self.collection.add(
            documents=[file_path], 
            embeddings=[embeddings], 
            metadatas=[{"asset_id": asset_id, "file_path": file_path}]
        )

    def retrieve_document_by_asset_id(self, asset_id: str):
        """Retrieve embeddings and document metadata by Asset ID."""
        results = self.collection.query(
            query_filter={"asset_id": asset_id}
        )
        return results
