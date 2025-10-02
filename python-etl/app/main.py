from modules.db_functions import db_utils
from modules.llm_call import ollama_utils
from modules.pdf_processing import *
import os
import requests
import ollama
import psycopg2
import pdfplumber
import re

if __name__ == "__main__":

    #retrieve database credentials from enviroment variables
    host = os.getenv("PG_HOST", "host does not exist")
    database = os.getenv("PG_NAME", "database does not exist")
    user = os.getenv("PG_USER_BACKEND", "user does not exist")
    password = os.getenv("PG_PASSWORD_BACKEND", "password does not exist")
    
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
    
    rg = ollama_utils(url = ollama_endpoint_url, model = ollama_model)
    
    landing_zone_path="/data/landing_zone"

    #iterate through files and perform llm call
    for file in os.listdir(landing_zone_path):
        abs_path_file=os.path.join(landing_zone_path, file)
        list_text, list_tables = process_pdf.extract_text_and_tables(abs_path_file,[],[])

        break
    

    print(list_tables[0])
    
    conn = dbu.db_connection(host=host, database=database, user=user, password=password)
    
    #answer = ollama_utils.query_ollama(user_input, ollama_endpoint_url, ollama_model)
    
    
    try:
        print("--Connecting to database--")
                
        # Execute query
        #dbu.db_execute_query(conn, create_table)    

        # Use parameterized query to avoid SQL injection
        #insert_query = "INSERT INTO electric_bills.user_input (input_text) VALUES (%s);"
        #dbu.db_execute_query(conn, insert_query, (user_input,))

        print("--All done, closing connection--")
        # Close the connection
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

