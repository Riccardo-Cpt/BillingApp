import json
import os
#import Code.ModelFunctions as mf
from modules.llm_functions import rag_functions
import train_data.electric_bill_training as train_data
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import psycopg2 
from modules.db_functions import db_utils
import datetime
import numpy as np
import requests

from psycopg2.extras import execute_values



if __name__ == '__main__':

    #retrieve database credentials from enviroment variables
    host = os.getenv("PG_HOST", "host does not exist")
    database = os.getenv("PG_NAME", "database does not exist")
    user = os.getenv("PG_USER_BACKEND", "user does not exist")
    password = os.getenv("PG_PASSWORD_BACKEND", "password does not exist")
    
    #retrieve ollama parameters
    ollama_endpoint_url=os.getenv("OLLAMA_ENDPOINT", "endpoint not received")
    ollama_model=os.getenv("OLLAMA_MODEL", "model not received")

    ollama_endpoint_url_embed=os.path.join(ollama_endpoint_url, "api/embed")

    rf = rag_functions(ollama_url = ollama_endpoint_url_embed, ollama_model = ollama_model)

    texts_for_embedding = rf.extract_context(train_data.contesto_bollette())

    embeddings_tuple = rf.compute_embeddings(texts_for_embedding)
    df_embeddings = pd.DataFrame(embeddings_tuple, columns=["cd_text_content", "vc_embedding"])

    df_embeddings['cd_document_name'] = 'electric_bill_context_sept2025'
    df_embeddings['vc_embedding'] = df_embeddings['vc_embedding'].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
    df_embeddings['vc_embedding'] = df_embeddings['vc_embedding'].apply(
    lambda x: x[0] if isinstance(x, list) and len(x) == 1 else x
    )
    df_embeddings['ts_creation'] = datetime.datetime.now()


    # Initialize the loader
    conn_params = {
        "host": host,
        "port" : "5432",
        "user" : user,
        "password" : password,
        "dbname": database
    }

    # Convert DataFrame to a list of tuples for execute_values
    data = list(df_embeddings[['cd_document_name', 'cd_text_content', 'vc_embedding', 'ts_creation']].itertuples(index=False, name=None))

    # SQL for insertion
    sql = """
        INSERT INTO embeddings.energy_bill_embeddings
        (cd_document_name, cd_text_content, vc_embedding, ts_creation)
        VALUES %s
    """

    # Connect and insert
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            # Use execute_values to insert all rows at once
            execute_values(
                cur,
                sql,
                data,
                template=None,
                page_size=100,
            )
        conn.commit()