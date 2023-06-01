#CreateEmbeddingService


# This service will be used to create embeddings for the given data.

#CreateEmbeddingService  shall create an object either of OpenEMbeddings or any other bert uncased embedding model
# and then call the create_embeddings method of that object to create embeddings for the given data.
from langchain.embeddings.openai import OpenAIEmbeddings
import transformers

class CreateEmbeddingService:
    def __init__(self):
        pass

    def create_embeddings(self, data, embedding_model):
        # Logic to create embeddings for the given data
        # Replace this with the actual implementation
        embedding_model = EmbeddingModelFactory().get_embedding_model(embedding_model)
        embeddings = embedding_model.create_embeddings(data)

        return embeddings
    
class EmbeddingModelFactory:
    def __init__(self):
        pass
    
    def get_embedding_model(self, embedding_model_name):
        # Logic to create the embedding model object
        if embedding_model_name == "OpenEmbeddings":
            embedding_model = OpenAIEmbeddings()
            return embedding_model
        elif embedding_model_name == "BertUncased":
            embedding_model = transformers.AutoModel.from_pretrained("bert-base-uncased")
            return embedding_model
        else:
            raise ValueError("Unsupported embedding model")