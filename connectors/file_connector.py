import pandas as pd
import os

class FileConnector:
    """Handles secure and dynamic data ingestion from local flat files."""
    
    # The __init__ method runs the moment we create a FileConnector object.
    # It takes the target file path as its single argument.
    def __init__(self, file_path: str):
        self.file_path = file_path
        # Immediately run a validation check before trying to do any work
        self._validate_file()

    # The underscore (_) before the name indicates this is a "private" method,
    # meant to be used internally by the class, not directly by the user.
    def _validate_file(self):
        # Check if the file actually exists on the operating system
        if not os.path.exists(self.file_path):
            # If it doesn't, crash gracefully with a clear error message
            raise FileNotFoundError(f"Error: The file {self.file_path} does not exist.")

    # This is the primary function we will call to get our data
    def load_data(self) -> pd.DataFrame:
        """Dynamically loads data into a Pandas DataFrame based on file extension."""
        
        # os.path.splitext splits "data.csv" into ["data", ".csv"]. 
        # [-1] grabs the last item (".csv") and .lower() ensures it matches our logic
        ext = os.path.splitext(self.file_path)[-1].lower()
        
        try:
            # Route the file to the correct Pandas reading engine based on its extension
            if ext == '.csv':
                return pd.read_csv(self.file_path)
            elif ext == '.parquet':
                return pd.read_parquet(self.file_path)
            elif ext == '.json':
                return pd.read_json(self.file_path)
            else:
                # Catch formats we haven't programmed into the tool yet
                raise ValueError(f"Unsupported file format: {ext}")
                
        except Exception as e:
            # If Pandas fails to read the file (e.g., corrupted file), print the error and return None
            print(f"Failed to load data: {e}")
            return None