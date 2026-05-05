# 🔍 MetaLens: Universal Data Observability Framework

**A plug-and-play Python engine for automated data profiling, statistical baselining, and exploratory data analysis across flat files and SQL databases.**

## 📖 Overview
In enterprise data environments, engineers spend hours performing repetitive Exploratory Data Analysis (EDA) on new datasets. **MetaLens** solves this by providing a unified, metadata-driven framework that automates the first four hours of data profiling. 

Whether extracting from a local CRM export or hooking directly into a massive production database, MetaLens dynamically adapts to the data source, intelligently samples the records, and outputs a clean, interactive HTML dashboard detailing the dataset's structural health and statistical distribution.

---

## 🏗️ Architecture & Core Components

This framework is built using object-oriented principles, separating ingestion adapters from the mathematical processing engine:

* **🔌 The Adapters (`connectors/`):**
  * `FileConnector`: Dynamically parses and ingests flat files (`.csv`, `.parquet`, `.json`).
  * `SqlConnector`: Uses `SQLAlchemy` to establish secure database connections and intelligently sample massive tables (preventing memory bottlenecks).
* **🧠 The Engine (`core/`):**
  * `DataProfiler`: Calculates "Analyst-Essential" metrics: Completeness (Null density), Cardinality (Unique counts), and Statistical Baselines (Min, Max, Mean, Std Dev).
  * `AutoVisualizer`: Reads the data types and utilizes `Plotly` to programmatically generate the appropriate interactive charts (e.g., box plots for numeric outliers, bar charts for categorical frequency).
* **⚙️ The Orchestrator (`main.py`):** Ties the modules together, manages environment variables, and executes the pipeline.

---

## 🛠️ Tech Stack & Requirements

* **Language:** Python 3.x
* **Data Processing:** `pandas`, `numpy`
* **Database Connection:** `sqlalchemy`, `psycopg2-binary` (PostgreSQL ready), `sqlite`
* **Visualization:** `plotly`
* **Security & Environment:** `python-dotenv`

---

## 🚀 Installation & Setup

To run MetaLens locally, you must configure a secure, hidden environment file to point the engine at your specific data paths.

### 1. Clone the Repository & Install Dependencies
```bash
git clone [https://github.com/AdelYa9/MetaLens.git](https://github.com/AdelYa9/MetaLens.git)
cd MetaLens
pip install -r requirements.txt
```

### 2. Configure Dynamic Environment Variables (Crucial Step)
This project relies on absolute local file paths that are kept out of version control for security. 
1. Create a new file in the root directory named exactly `.env`
2. Add your target data path to the file. For example:
```text
NEXUS_DATA_PATH="C:\path\to\your\local\data.csv"
```
*(Note: The `.gitignore` file is already configured to ensure your `.env` file is never pushed to GitHub).*

---

## 📊 Usage & Execution

Once your `.env` file is configured, simply run the main orchestrator:

```bash
python main.py
```

**What happens next?**
1. The framework spins up a temporary SQLite database.
2. It ingests the data designated in your `.env` file and pushes it into the database.
3. The `SqlConnector` samples the data.
4. The `DataProfiler` and `AutoVisualizer` generate a complete health report.
5. An interactive dashboard is exported to `output/sql_observability_report.html`.

---

## 🗺️ Portfolio Context & Lineage

MetaLens serves as the "connective tissue" in my Enterprise Data Engineering portfolio:
* **Predecessor:** It successfully profiled the Gold Layer JSON-to-CSV output from **Project Nexus** (ETL Data Lake).
* **Successor:** It is designed with PostgreSQL compatibility to provide immediate Data Observability for my upcoming **FinTech SQL Vault** (Enterprise Star Schema Database) project.