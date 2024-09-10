import gensim
import numpy as np

class EmbeddingService:
    def __init__(self):
        # Load pre-trained word2vec model
        self.model = gensim.models.KeyedVectors.load_word2vec_format(
            'path/to/word2vec.bin', binary=True
        )

    def generate_embeddings(self, document_content):
        words = document_content.split()
        embedding_dim = self.model.vector_size
        # Generate word embeddings and average them to form a document embedding
        embeddings = []
        for word in words:
            if word in self.model.key_to_index:
                embeddings.append(self.model[word])
            else:
                embeddings.append(np.zeros(embedding_dim))
        
        # Average embeddings to represent the document
        document_embedding = np.mean(embeddings, axis=0)
        return document_embedding
