import ollama
import requests
import os
from sklearn.metrics.pairwise import cosine_similarity

import ollama
import requests
import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ollama_utils:
    def __init__(self, url, model):
        self.embedding_model = 'nomic-embed-text'  # Model used for embeddings
        self.model = model  # Model used for generation
        self.ollama_endpoint_url_embed = os.path.join(url, "api/embed")  # Endpoint for embeddings
        self.ollama_endpoint_url_generate = os.path.join(url, "api/generate")  # Endpoint for generation

    # Calls Ollama's generate API to get a response for a given prompt
    def call_ollama_api_generate(self, prompt):
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        }
        response = requests.post(self.ollama_endpoint_url_generate, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["response"]

    # Calls Ollama's embeddings API to get embeddings for a given input text
    def call_ollama_api_embedding(self, input_text):
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.embedding_model,
            "input": input_text
        }
        response = requests.post(self.ollama_endpoint_url_embed, headers=headers, json=data)

        return response.json()["embeddings"]

    # Computes embeddings for input dictionary of text chunks. The input is dictionary because derived from extracted tables
    def compute_embeddings(self, chunk_texts: dict):
        embeddings = []
        for original_text, chunk in chunk_texts.items():
            embedding = self.call_ollama_api_embedding(chunk)
            embedding_array = np.asarray(embedding, dtype=np.float32)
            embeddings.append((original_text, embedding_array))

        return tuple(embeddings)

    # Extracts text from a list of JSON strings for embedding
    def extract_context(self, context_list):
        texts_for_embedding = {}
        for json_str in context_list:
            try:
                json_obj = json.loads(json_str)
                text_parts = []
                for value in json_obj.values():
                    if isinstance(value, dict):
                        text_ports.extend(v for v in value.values() if isinstance(v, str))
                    elif isinstance(value, str):
                        text_parts.append(value)
                texts_for_embedding[json_str] = " ".join(text_parts)
            except json.JSONDecodeError as e:
                raise Exception(f"JSON string not correctly parsed: {e}")
            
        return texts_for_embedding

    # Retrieves the top_k most relevant chunks based on cosine similarity between query and embedded chunks