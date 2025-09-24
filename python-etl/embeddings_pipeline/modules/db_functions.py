import psycopg2
import pandas as pd
from sqlalchemy import create_engine

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
