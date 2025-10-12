import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from psycopg2.extras import RealDictCursor
import numpy as np


class db_utils:

    def __init__(self, host: str, port: str, username: str, password: str, db_name: str):
        """
        Initialize the PostgresLoader with connection parameters.

        Args:
            host: PostgreSQL host (e.g., "localhost" or IP).
            port: PostgreSQL port (e.g., "5432").
            username: PostgreSQL username.
            password: PostgreSQL password.
            db_name: PostgreSQL database name.
        """

        self.conn = {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "db_name": db_name,
        }
        self.engine = self._create_engine()

    def db_connection(self):
        """Establish a connection to the PostgreSQL database."""
        conn_params = {
            "host": self.conn["host"],
            "port": self.conn["port"],
            "user": self.conn["username"],
            "password": self.conn["password"],
            "dbname": self.conn["db_name"],
        }
        return psycopg2.connect(**conn_params)
    
    def _create_engine(self):
        """Create a SQLAlchemy engine using the connection parameters."""
        return create_engine(
            f"postgresql+psycopg2://{self.conn['username']}:{self.conn['password']}@"
            f"{self.conn['host']}:{self.conn['port']}/{self.conn['db_name']}"
        )

    def load_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: str = "public",
        if_exists: str = "fail",
        index: bool = False,
        chunksize: int = None,
        dtype: dict = None,
    ) -> None:
        """
        Load a pandas DataFrame into a PostgreSQL table, optionally specifying a schema.

        Args:
            df: Pandas DataFrame to load.
            table_name: Name of the target table in PostgreSQL.
            schema: Name of the schema in PostgreSQL (default: "public").
            if_exists: What to do if the table already exists. Options: "fail", "replace", "append".
            index: Write DataFrame index as a column.
            chunksize: Rows to write at a time (for large DataFrames).
            dtype: SQL data types for columns (optional).
        """
        df.to_sql(
            name=table_name,
            con=self.engine,
            schema=schema,  # Pass the schema here
            if_exists=if_exists,
            index=index,
            chunksize=chunksize,
            dtype=dtype,
        )
        print(f"Data loaded to {schema}.{table_name} successfully!")

    def find_most_similar_embedding(
        self,
        embedding: np.ndarray,
        schema: str,
        table: str,
        array_column: str,
        text_column: str,
        similarity_type: str = "<=>",
        top_k: int = 1,
    ) -> list[dict]:
        """
        Find the most similar embedding(s) in a PostgreSQL table using cosine similarity.

        Args:
            embedding: Input embedding as a NumPy array (dtype=np.float32).
            schema: PostgreSQL schema name.
            table: PostgreSQL table name.
            array_column: Name of the vector column in the table (default: "vc_array").
            text_column: Name of the text column to return (default: "cd_text_content").
            top_k: Number of most similar embeddings to return (default: 1).

        Returns:
            List of dictionaries, each containing the text and similarity score.
        """
        # Convert the input embedding to a list for SQL query
        embedding_list = embedding.tolist()
        if isinstance(embedding_list[0], list) and len(embedding_list) == 1:
            embedding_list = embedding_list[0]  # Flatten if nested

        # SQL query using the <=> operator for cosine distance
        query = f"""
            SELECT
                {text_column},
                1 - ({array_column} {similarity_type} CAST(%s AS vector)) AS cosine_similarity
            FROM
                {schema}.{table}
            ORDER BY
                {array_column} {similarity_type} CAST(%s AS vector)
            LIMIT %s;
        """

        #define connection with db
        conn = self.db_connection()


        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (embedding_list, embedding_list, top_k))
                results = cur.fetchall()
            return results
        finally:
            conn.close()