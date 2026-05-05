import pandas as pd
import plotly.express as px
import os

class AutoVisualizer:
    """Generates an automated, interactive HTML Data Observability Report."""
    
    def __init__(self, df: pd.DataFrame, summary_df: pd.DataFrame):
        self.df = df
        self.summary_df = summary_df

    def _generate_plots(self) -> str:
        """Determines the correct chart type based on column dtype and cardinality."""
        plot_html = ""
        
        # Iterate through every column in the dataset
        for col in self.df.columns:
            
            # RULE 1: If the data is numeric, generate a Histogram with a Box Plot
            if pd.api.types.is_numeric_dtype(self.df[col]):
                fig = px.histogram(
                    self.df, 
                    x=col, 
                    marginal="box", # Adds a box plot above the histogram to spot outliers
                    title=f"Distribution & Outliers: {col}",
                    color_discrete_sequence=['#005B96'] # Clean, professional blue
                )
                # Convert the interactive Plotly figure to an HTML string
                plot_html += fig.to_html(full_html=False, include_plotlyjs='cdn')
            
            # RULE 2: If the data is categorical (text) and has low cardinality (< 20 unique values)
            elif pd.api.types.is_object_dtype(self.df[col]) and self.df[col].nunique() < 20:
                # Calculate the frequency of each category
                counts = self.df[col].value_counts().reset_index()
                counts.columns = [col, 'Frequency']
                
                fig = px.bar(
                    counts, 
                    x=col, 
                    y='Frequency', 
                    title=f"Categorical Frequency: {col}",
                    color_discrete_sequence=['#03396C']
                )
                plot_html += fig.to_html(full_html=False, include_plotlyjs='cdn')
                
        return plot_html

    def export_html_report(self, output_path: str = "output/metalens_report.html"):
        """Compiles the summary table and plots into a final deliverable report."""
        
        print("Rendering interactive visualizations...")
        
        # Build the HTML architecture
        html_content = f"""
        <html>
        <head>
            <title>MetaLens Observability Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }}
                h1, h2 {{ color: #333; }}
                .container {{ background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 40px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #005B96; color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 MetaLens Data Observability Report</h1>
                <p>Automated statistical baselining and profile generation.</p>
                <hr>
                
                <h2>1. Statistical Health Summary</h2>
                {self.summary_df.to_html(classes='table')}
                
                <h2>2. Feature Distributions</h2>
                {self._generate_plots()}
            </div>
        </body>
        </html>
        """
        
        # Ensure the 'output' directory exists before saving
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the compiled HTML to the local machine
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Success! Report generated at: {output_path}")