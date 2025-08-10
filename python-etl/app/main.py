from modules.db_functions import DBUtils
import os

if __name__ == "__main__":
    
    #retrieve database credentials from enviroment variables
    host = os.getenv("PG_HOST", "host does not exist")
    database = os.getenv("PG_NAME", "database does not exist")
    user = os.getenv("PG_USER_BACKEND", "user does not exist")
    password = os.getenv("PG_PASSWORD_BACKEND", "password does not exist")
    
    
    print(host, database, user, password)

    create_table = """CREATE TABLE IF NOT EXISTS electric_bills.user_input (
                    id SERIAL PRIMARY KEY,
                    input_text TEXT NOT NULL);"""
    
    
    #ask the user to insert something in the database
    user_input = "ciao"
    
    
    conn = DBUtils.db_connection(host=host, database=database, user=user, password=password)
    
    
    try:
        print("--Connecting to database--")
                
        # Execute query
        #DBUtils.db_execute_query(conn, create_table)    

        # Use parameterized query to avoid SQL injection
        #insert_query = "INSERT INTO electric_bills.user_input (input_text) VALUES (%s);"
        #DBUtils.db_execute_query(conn, insert_query, (user_input,))

        print("--All done, closing connection--")
        # Close the connection
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

