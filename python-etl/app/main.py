from modules.db_functions import db_utils
from modules.llm_call import ollama_utils
from modules.pdf_processing import *
import os
import requests
import ollama
import psycopg2
import pdfplumber
import re
import pandas as pd
import datetime

def get_relevant_chunks(self, query, schema, table_name, vector_column, context_column, top_k=1):
    """
    Retrieves the top_k most relevant chunks from a PostgreSQL table based on cosine similarity between the query embedding and stored embeddings.

    Args:
        query (str): The input query to find relevant chunks for.
        schema (str): The schema name in PostgreSQL.
        table_name (str): The table name in PostgreSQL.
        vector_column (str): The column name containing the embeddings.
        context_column (str): The column name containing the context text.
        top_k (int): Number of relevant chunks to retrieve (default: 1).

    Returns:
        list: A list of the top_k relevant context strings.
    """
    # Get the embedding for the query
    query_embedding = np.array(self.call_ollama_api_embedding(query))

    # Establish a connection to the database
    conn = self.db_connection(
        host=self.conn["host"],
        database=self.conn["db_name"],
        user=self.conn["username"],
        password=self.conn["password"]
    )

    # Create a cursor
    cur = conn.cursor()

    # Query to find the top_k most similar embeddings using cosine similarity
    # Note: This assumes you have the pgvector extension installed and the vector column is of type 'vector'
    sql = f"""
        SELECT {context_column}
        FROM {schema}.{table_name}
        ORDER BY {vector_column} <=> %s
        LIMIT %s;
    """

    # Execute the query
    cur.execute(sql, (query_embedding, top_k))

    # Fetch the results
    results = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Extract the context from the results
    relevant_chunks = [result[0] for result in results]

    return relevant_chunks



"""This pipeline does:
    1. From input prompt computes embeddings
    2. Use cosine similarity to find in RAG in vector database postgres
    3. Make the actual prompt to the model consisting of RAG output + original prompt
    4. Store the JSON output in a pandas

"""
def rag_pipeline(prompt, context_list, ollama_url, model):
    # Initialize Ollama utils
    ollama_client = ollama_utils(ollama_url, model)

    # Step 1: Extract context from JSON strings
    texts_for_embedding = ollama_client.extract_context(context_list)

    # Step 2: Compute embeddings for context chunks
    embeddings = ollama_client.compute_embeddings(texts_for_embedding)

    # Step 3: Get relevant chunks based on cosine similarity
    relevant_chunks = ollama_client.get_relevant_chunks(prompt, embeddings, texts_for_embedding, top_k=1)

    # Step 4: Build the augmented prompt
    augmented_prompt = f"Context: {relevant_chunks[0]}\n\nQuestion: {prompt}"

    # Step 5: Call Ollama's generate API with the augmented prompt
    response = ollama_client._call_ollama_api_generate(augmented_prompt)

    # Return the final output in JSON format
    return {
        "prompt": prompt,
        "retrieved_context": relevant_chunks,
        "response": response
    }




if __name__ == "__main__":

    #retrieve database credentials from enviroment variables
    host = os.getenv("PG_HOST", "host does not exist")
    database = os.getenv("PG_NAME", "database does not exist")
    user = os.getenv("PG_USER_BACKEND", "user does not exist")
    password = os.getenv("PG_PASSWORD_BACKEND", "password does not exist")
    embedding_schema="embeddings"
    landing_schema="landing"
    loading_schema="in_electric_bills"
    
    #retrieve ollama parameters
    ollama_endpoint_url=os.getenv("OLLAMA_ENDPOINT", "endpoint not received")
    ollama_model=os.getenv("OLLAMA_MODEL", "model not received")

    #Initialize classes    
    process_pdf = process_pdf()
    dbu = db_utils(host = host,
            port = "5432",
            username = user,
            password = password,
            db_name = database,
        )
    
    ou = ollama_utils(url = ollama_endpoint_url, model = ollama_model)
    
    landing_zone_path="/data/landing_zone"

    #iterate through files and perform llm call
    for file in os.listdir(landing_zone_path):
        abs_path_file=os.path.join(landing_zone_path, file)
        list_text, list_tables = process_pdf.extract_text_and_tables(abs_path_file,[],[])

        #for each free text derived from a table, perform the RAG
        for text_table in list_tables:
            dict_table = {"table" : text_table}
            embedding_prompt_tuple = ou.compute_embeddings(dict_table)

            #extract the embedding related to table text
            embedded_prompt = embedding_prompt_tuple[0][1]

            #Retrieve augmented context associated to prompt from the database
            results = dbu.find_most_similar_embedding(
                                                    embedded_prompt,
                                                    schema=loading_schema,
                                                    table="energy_bill_embeddings",
                                                    array_column="vc_embedding",
                                                    text_column="cd_text_content",
                                                    top_k=1,
                                                    similarity_type = "<=>" #cosine similarity
                                                
                                                )

            # Extract the JSON string from the output and parse the json
            data = json.loads(results[0]['cd_text_content'])
            # Dynamically get the first key in the dictionary. This key is associated with the subject of extracted context
            context_subject = next(iter(data))
            # Extract the nested dictionary using the dynamic key
            rag_context = data[context_subject]

            #Generate a prompt from initial table extracted text + RAG text
            composed_prompt = f"""Ti viene fornito uil seguente testo:{text_table}
            Obbiettivo: Devi rimpiazzare il testo in seguito tra apici con informazioni estratte dal testo precedente. Le informazioni aggiuntive non servono, ignorale. Non generare spiegazioni:{rag_context}
            """

            response = ou.call_ollama_api_generate(composed_prompt)
            # Parse the string into a dictionary using list comprehension
            # Only split lines that contain ':'
            json_response = {
                k.strip(): v.strip()
                for line in response.strip().split('\n')
                if ':' in line
                for k, v in [line.split(':', 1)]
            }

            # Create a DataFrame
            df_response = pd.DataFrame([json_response])
            df_response["TS_INGESTION"]=datetime.datetime.now()
            df_response["INPUT_FILE_NAME"]=file
            print(f"Si sta elaborando: {context_subject}")
            print(f"Risposta ottenuta da llm: {json_response}")
            
            #extract the table where data converted in dataframe should be loaded
            db_table_name=dbu.rag_mapping_to_db(context_subject)

            #################################################
            #SKIPPING ANY DATA QUALITY TO EVALUATE THE OUTPUT
            #################################################


            # TO DO: CREATE EMPTY DATAFRAMES WITH FIXED SCHEMA BEFORE ITERATING OVER FILES.
            # AT EACH ITERATION ADD A NEW ROW TO THE DATAFRAME
            # AT THE END OF ITERATIONS LOAD ALL DATA FROM DATAFRAMES INTO TABLES

            #Load data in dataframe into postgres table
            try:
                dbu.load_dataframe(
                        df=df_response,
                        table_name=db_table_name.lower(),#lower function to create an object in lowercase characters in postgres
                        schema=landing_schema,
                        if_exists = "append",
                        index= False,
                        chunksize = None,
                        dtype= None
                )
            
            except Exception as e:
                print(f"No data will be loaded into table: {db_table_name}")



            #break
        break
    

