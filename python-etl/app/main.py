from modules.db_functions import db_utils as dbu
from modules.llm_call import *
from modules.text_parsing import *
import os
import requests
import ollama
import psycopg2
import pdfplumber
import re

if __name__ == "__main__":
    
    print(os. getcwd())
    
    landing_zone_path="./Data/landing_zone"
    
    #retrieve database credentials from enviroment variables
    host = os.getenv("PG_HOST", "host does not exist")
    database = os.getenv("PG_NAME", "database does not exist")
    user = os.getenv("PG_USER_BACKEND", "user does not exist")
    password = os.getenv("PG_PASSWORD_BACKEND", "password does not exist")
    
    #retrieve ollama parameters
    ollama_endpoint_url=os.getenv("OLLAMA_ENDPOINT", "endpoint not received")
    ollama_model=os.getenv("OLLAMA_MODEL", "model not received")
    
    print(host, database, user, password, ollama_endpoint_url, ollama_model)

    create_table = """CREATE TABLE IF NOT EXISTS electric_bills.user_input (
                    id SERIAL PRIMARY KEY,
                    input_text TEXT NOT NULL);"""
    
    
    #ask the user to insert something in the database
    user_input = "ciao"
    
    
    conn = dbu.db_connection(host=host, database=database, user=user, password=password)
    
    answer = ollama_utils(user_input, ollama_endpoint_url, ollama_model)
    print(answer)
    
    
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

