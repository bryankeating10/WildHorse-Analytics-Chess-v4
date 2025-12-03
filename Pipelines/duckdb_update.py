# Establish project root and add to PATH
from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0,(str(project_root)))

# Import dependencies
import pandas as pd
import duckdb

# Username
user1 = "kingsk4"
username = "kingsk4_2025_depth20"

# Create DuckDB database and load processed data
con = duckdb.connect(f'{project_root}/Data/Gold/{username}.duckdb')
con.execute(f"""
    CREATE TABLE IF NOT EXISTS meta AS 
    SELECT * FROM read_csv_auto('{project_root}/Data/Gold/{user1}_meta_gold.csv');
""")
print("="*50)
print("DuckDB Database Metadata Table Complete")
print("="*50)
print()
con.execute(f"""
    CREATE TABLE IF NOT EXISTS moves AS
    SELECT * FROM read_csv_auto('{project_root}/Data/Gold/{user1}_moves_gold.csv');
""")
print("="*50)
print("DuckDB Database Moves Table Complete")
print("="*50)
print()
con.close()