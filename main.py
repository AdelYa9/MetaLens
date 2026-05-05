import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Import our custom classes from the framework
from connectors.file_connector import FileConnector
from connectors.sql_connector import SqlConnector
from core.profiler import DataProfiler
from core.visualizer import AutoVisualizer

def test_sql_pipeline(csv_source_path: str):
    """Tests the full SQL ingestion and profiling pipeline using a local SQLite instance."""
    
    print("--- 1. Setting up temporary SQLite Database for testing ---")
    # Create a local SQLite database file in the output folder
    sqlite_uri = "sqlite:///output/test_fintech.db"
    temp_engine = create_engine(sqlite_uri)
    
    # Load the CSV and push it into the database to simulate a real SQL table
    dummy_data = pd.read_csv(csv_source_path)
    dummy_data.to_sql('transactions', temp_engine, if_exists='replace', index=False)
    print("Database ready. Table 'transactions' created.\n")

    print("--- 2. Initiating MetaLens SQL Profiling ---")
    # Point our SqlConnector at the new database and sample the data
    ingestor = SqlConnector(sqlite_uri)
    df = ingestor.load_data_sample(table_name="transactions", sample_size=5000)
    
    if df is not None:
        print(f"SQL Data Sample Loaded Successfully. Shape: {df.shape}")
        
        # 3. Math Engine: Generate statistical baselines
        profiler = DataProfiler(df)
        health_summary = profiler.generate_summary()
        
        # Print summary to console for immediate feedback
        print("\n--- MetaLens Data Health Summary ---")
        print(health_summary.to_string())
        
        # 4. Visualizer Engine: Generate the interactive HTML dashboard
        visualizer = AutoVisualizer(df, health_summary)
        visualizer.export_html_report("output/sql_observability_report.html")

if __name__ == "__main__":
    
    # 1. Look for the hidden .env file and load its contents into system memory
    load_dotenv()
    
    # 2. Fetch the specific file path string associated with our target variable
    nexus_data_path = os.getenv("NEXUS_DATA_PATH")
    
    # 3. Safety Check: Ensure the path was actually found
    if not nexus_data_path:
        raise ValueError("Error: Environment variable NEXUS_DATA_PATH is not set in the .env file.")
    
    # 4. Execute the pipeline
    test_sql_pipeline(nexus_data_path)