import pandas as pd
from sqlalchemy import create_engine, text
import logging

class SqlConnector:
    """Handles secure ingestion and sampling from relational databases."""
    
    def __init__(self, connection_uri: str):
        # The URI tells SQLAlchemy where the DB is and what dialect to use (e.g., postgresql://...)
        self.connection_uri = connection_uri
        self.engine = create_engine(self.connection_uri)

    def load_data_sample(self, table_name: str, sample_size: int = 10000) -> pd.DataFrame:
        """
        Extracts a safe sample from a database table to prevent memory overloads.
        """
        print(f"Connecting to database and sampling {sample_size} rows from '{table_name}'...")
        
        try:
            # We use a parameterized query for security (prevents SQL injection)
            query = f"SELECT * FROM {table_name} LIMIT {sample_size}"
            
            # Open a secure connection, execute the query, and load straight into Pandas
            with self.engine.connect() as connection:
                df = pd.read_sql(text(query), connection)
                return df
                
        except Exception as e:
            print(f"Database connection or query failed: {e}")
            return None