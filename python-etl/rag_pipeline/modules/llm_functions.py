class rag_functions():
    def compute_embeddings(chunk_texts = []):
        embeddings = []
        for i, chunk in enumerate(chunk_texts):
          # Call Ollama's embeddings API
          response = ollama.embeddings(
              model='nomic-embed-text', # Specify the embedding model
              prompt=chunk               # The text you want to embed
          )
          # The embedding is a list of floats
          embedding = response['embedding']
          embeddings.append(embedding)
          #convert embeddings as numpy array where each element is of type numpy.float32
          embedding_array = np.asarray(embeddings, dtype=np.float32)
        return embedding_array, chunk_texts

    def extract_context(context_list):

        texts_for_embedding=[]
        for json_str in td.contesto_bollette():
            try:
                json_obj = json.loads(json_str)
                # Extract all string values from the JSON object
                text_parts = []
                for value in json_obj.values():
                    if isinstance(value, dict):
                        text_parts.extend(v for v in value.values() if isinstance(v, str))
                    elif isinstance(value, str):
                        text_parts.append(value)
                texts_for_embedding.append(" ".join(text_parts))
            except json.JSONDecodeError:
                texts_for_embedding.append("")  # Handle invalid JSON if needed

        return texts_for_embedding


    # This function retrieves the top_k most relevant chunks based on cosine similarity between query and embedded chuncks
    def getRelevantChunksTesting(query, embedding_array, chunk_texts, top_k=3):
       
      #Compute embeddings
      query_embedding = np.array(ollama.embeddings(model='nomic-embed-text', prompt=query)['embedding'])
      #Simple cosine similarity. Used for chunck tuning. I does not store the embedding array
      # Compute cosine similarity between user query and embedded chunks
      similarities = cosine_similarity([query_embedding], embedding_array)
      # Obtain the indices for those chunks with the k highest similarity scores
      top_indices = np.argsort(similarities)[0][-top_k:][::-1]
      retrieved_chunks = [chunk_texts[i] for i in top_indices]
      
      return retrieved_chunks
