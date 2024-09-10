# momentum_backend_assignment
These instructions will help you set up the environment for running the Document Processing and 
Chatbot API using FastAPI, LangChain, ChromaDB, and Word2Vec embeddings.

1. Prerequisites: Ensure that you have Python 3.9 or higher installed on your machine. You can download 
it from official website which is https://www.python.org/downloads/

Verify Python installation by running: python --version


2. Clone the Repository:Clone the repository that contains the code for the Document Processing and 
Chatbot API.
git clone https://github.com/akbundi/momentum_backend_assignment
cd document_processing_service

3. Install Dependencies:All the necessary dependencies are listed in the requirements.txt file. Run the following command to install them:
pip install -r requirements.txt

3.1 Install Other necessary Dependencies:-
Make sure to install the required libraries for LangChain and FastAPI:
pip install langchain fastapi uvicorn transformers gensim

4.Download Word2Vec Weights:You need to download the Word2Vec model as mentioned in the system overview. You can use Gensim to load Word2Vec weights.
Follow these steps:

Visit the Word2Vec HuggingFace repository present at https://huggingface.co/vocab-transformers/distilbert-word2vec_256k-MLM_1M/tree/main/word2vec
Download the Word2Vec model weights (word2vec_weights.bin).
Save the model to a directory, for example: models/word2vec/.

You can load the model in your Python code using Gensim:
from gensim.models import KeyedVectors

# Load pre-trained Word2Vec embeddings
word2vec_model = KeyedVectors.load_word2vec_format('models/word2vec/word2vec_weights.bin', binary=True)

5. Start the API:The main entry point for the FastAPI app is main.py. Start the FastAPI server using Uvicorn:
uvicorn main:app --reload
6. Testing the API:

6.1 Accessing FastAPI Documentation:
FastAPI provides automatic documentation through OpenAPI. Once the server is running, you can access the API documentation in your browser at:
http://localhost:8000/docs

6.2 Using Postman:
Import the Postman collection that was provided (document_processing_and_chatbot_api.postman_collection.json).
Make sure that the base URL is set to http://localhost:8000.
Test each API endpoint:
Document Processing: Test the /api/documents/process endpoint by providing the path to a document.
Chat Service: Test the /api/chat/start, /api/chat/message, and /api/chat/history endpoints.

7. Setting Up the Vector Database:
The vector database used is ChromaDB, and its data is stored in the local directory ./vector_db. There’s no need for an additional setup beyond installing ChromaDB via pip.

Make sure the following directory structure is created automatically upon running the app:
vector_db/
├── documents
└── embeddings
If the vector database doesn’t initialize correctly, ensure the persist directory is defined in your VectorDBService:
self.client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./vector_db"
))
8. Additional Configurations :
To store configuration settings such as file paths, API keys, or other environment-specific variables, consider using a .env file with the python-dotenv package.
1.Install python-dotenv:pip install python-dotenv
2.Create a .env file in your project root:VECTOR_DB_DIRECTORY=./vector_db
MODEL_DIRECTORY=./models/word2vec/

3.Load the environment variables in your code:
from dotenv import load_dotenv
import os

load_dotenv()

vector_db_directory = os.getenv("VECTOR_DB_DIRECTORY")

9.Running Unit Tests:use the pytest framework to run tests:

pip install pytest
pytest

10.Deploying the Service :
Once the service is running locally, you can containerize it with Docker for easier deployment.
1.
# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port 8000 and start the server
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
2.Build and run the Docker container:

docker build -t document-chat-api .
docker run -p 8000:8000 document-chat-api


