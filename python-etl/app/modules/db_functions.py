import psycopg2 

class db_utils:

    @staticmethod
    def db_connection(host, database, user, password):
        """Establish a connection to the PostgreSQL database."""
        conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            
        return conn

    @staticmethod
    def db_execute_query(conn, query, params=None):
        """Execute a given SQL query using the provided database connection."""

        with conn.cursor() as cur:
            try:
                cur.execute(query, vars=params)
                conn.commit()

            except Exception as e:
                print(f"An error occurred while executing the query: {e}")
                if conn:
                    conn.rollback()
            finally:
                if cur:
                    cur.close()