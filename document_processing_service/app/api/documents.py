# app/api/documents.py
from fastapi import APIRouter, HTTPException
from app.core.file_handler import FileHandler
from app.core.embedding_service import EmbeddingService
from app.core.vector_db_service import VectorDBService

router = APIRouter()

@router.post("/api/documents/process")
async def process_document(file_path: str):
    file_handler = FileHandler()
    try:
        # Step 1: Read file
        document_content = file_handler.read_file(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Step 2: Generate embeddings
    embedding_service = EmbeddingService()
    embeddings = embedding_service.generate_embeddings(document_content)

    # Step 3: Store embeddings in vector database
    vector_db_service = VectorDBService()
    asset_id = vector_db_service.store_embeddings(embeddings, metadata={"file_path": file_path})

    return {"asset_id": asset_id}
