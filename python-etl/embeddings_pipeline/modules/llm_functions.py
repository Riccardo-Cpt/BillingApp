import json
import ollama
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests

class rag_functions:

    def __init__(self, ollama_url, ollama_model):
        self.url = ollama_url
        self.model = ollama_model
        self.embedding_model = "nomic-embed-text"

    
    def _call_ollama_api_embedding(self, input_text):
            headers = {"Content-Type": "application/json"}
            
            data = {
                "model": self.embedding_model, #nomic-embed-text alternative for bigger embeddings
                "input" : input_text
            }

            response = requests.post(self.url, headers=headers, json=data)

            return response.json()["embeddings"]

    def compute_embeddings(self, chunk_texts:dict):
        embeddings = []
        for original_text, chunk in chunk_texts.items():
            # Call Ollama's embeddings API            
            embedding = self._call_ollama_api_embedding(chunk)

            # The embedding is a list of floats
            embedding_array = np.asarray(embedding, dtype=np.float32)
            embeddings.append((original_text, embedding_array))

        return tuple(embeddings) #embedding_array, chunk_texts

    def extract_context(self, context_list):
        texts_for_embedding = {}
        for json_str in context_list:
            try:
                json_obj = json.loads(json_str)
                text_parts = []
                for value in json_obj.values():
                    if isinstance(value, dict):
                        text_parts.extend(v for v in value.values() if isinstance(v, str))
                    elif isinstance(value, str):
                        text_parts.append(value)
                # Use the original JSON string as the key
                texts_for_embedding[json_str] = " ".join(text_parts)
            except json.JSONDecodeError as e:
                raise Exception(f"JSON string not correctly parsed: {e}")
        return texts_for_embedding


    # This function retrieves the top_k most relevant chunks based on cosine similarity between query and embedded chuncks
    def getRelevantChunksTesting(self, query, embedding_array, chunk_texts, top_k=1):
    
      prompt_embedding = response = self.call_ollama_api_embedding(self, query)

      #Compute embeddings
      query_embedding = np.array(prompt_embedding)
      #Simple cosine similarity. Used for chunck tuning. I does not store the embedding array
      # Compute cosine similarity between user query and embedded chunks
      similarities = cosine_similarity([query_embedding], embedding_array)
      # Obtain the indices for those chunks with the k highest similarity scores
      top_indices = np.argsort(similarities)[0][-top_k:][::-1]
      retrieved_chunks = [chunk_texts[i] for i in top_indices]
      
      return retrieved_chunks

