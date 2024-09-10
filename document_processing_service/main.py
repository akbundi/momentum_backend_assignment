from file_handler import FileHandler
from embedding_service import EmbeddingService
from vector_db_service import VectorDBService

def main(file_path):
    # Step 1: Read file content
    file_handler = FileHandler()
    document_content = file_handler.read_file(file_path)
    
    # Step 2: Generate embeddings
    embedding_service = EmbeddingService()
    embeddings = embedding_service.generate_embeddings(document_content)
    
    # Step 3: Store embeddings in vector database
    vector_db_service = VectorDBService()
    asset_id = vector_db_service.store_embeddings(embeddings, metadata={"file_path": file_path})
    
    print(f"Document processed and stored with Asset ID: {asset_id}")

if __name__ == "__main__":
    # Test the service with a sample file
    file_path = "path/to/your/document.pdf"  # Modify this as needed
    main(file_path)
