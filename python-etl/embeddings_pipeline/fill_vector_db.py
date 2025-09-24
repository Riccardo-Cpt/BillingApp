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

import requests


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
    df_embeddings = pd.DataFrame(embeddings_tuple, columns=["text", "embedding"])
    df_embeddings['embedding'] = df_embeddings['embedding'].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)


    # Initialize the loader
    loader = db_utils(
        host=host,
        port="5432",
        username=user,
        password=password,
        db_name=database,
    )

    # Load data
    loader.load_dataframe(df=df_embeddings, schema = "in_electric_bills", table_name="energy_bill_embeddings", if_exists="append")