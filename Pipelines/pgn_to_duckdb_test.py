"""
Full data pipeline up to DuckDB database creation. Ingests PGN files from user archives URL, converts them 
into move-level and game-level DataFrames, adds Stockfish evaluations, and processes them for memory efficiency.
"""

# Establish project root and add to PATH
from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0,(str(project_root)))

# Import dependencies
import pandas as pd
import duckdb

# Import custom modules
from Ingestion.download_pgn import download_pgn
from Ingestion.movedata import MoveData
from Ingestion.metadata import MetaData
from Processing.cleanmeta import remove_unnec, convert_datetime, map_results, map_termination
from Processing.cleanmove import convert_color
from Processing.unique_fen import unique_fens, repopulate_unique_evals
from Processing.add_eval import add_eval, add_eval_to_series

# Username
username = "bkgr03"

# Download PGN files from user archives from December 2025 onwards
download_pgn(username, start_date='2025-12')
username = username.lower()
if len(username) > 8:
    username = username[:8]

print()
print("="*50)
print("PGN Download Complete")
print("="*50)
print()

# Metadata extraction
meta_parser = MetaData(f'{project_root}/Data/Bronze/{username}.pgn')
meta_parser.save_csv(f'{project_root}/Data/Silver/{username}_meta.csv')
print()
print("="*50)
print("Metadata Extraction Complete")
print("="*50)
print()

# Move data extraction
move_parser = MoveData(f'{project_root}/Data/Bronze/{username}.pgn')
move_parser.save_csv(f'{project_root}/Data/Silver/{username}_moves.csv')

print("="*50)
print("Move Data Extraction Complete")
print("="*50)
print()

# Process metadata
meta_df = meta_parser.df
meta_df = remove_unnec(meta_df)
meta_df = convert_datetime(meta_df)
meta_df = map_results(meta_df)
meta_df = map_termination(meta_df)
meta_df.to_csv(f'{project_root}/Data/Gold/{username}_meta_gold.csv', index=False)
print("="*50)
print("Metadata Processing Complete")
print("="*50)
print()

# Process move data
move_df = move_parser.df
move_df = convert_color(move_df)
print("="*50)
print("Adding Stockfish Evaluations...")
print("="*50)

# Extract unique FENs and to avoid redundant evaluations
unique_series = unique_fens(move_df)
print()

# Add evaluations to unique FENs
unique_series = add_eval_to_series(unique_series, depth=5)
print(unique_series.head())


# Repopulate evaluations back to move dataframe
print(move_df.head())
move_df = repopulate_unique_evals(move_df, unique_series)
print(move_df.head())

move_df.to_csv(f'{project_root}/Data/Gold/{username}_moves_gold.csv', index=False)
print("="*50)
print("Move Data Processing Complete")
print("="*50)
print()

# # Create DuckDB database and load processed data
# con = duckdb.connect(f'{project_root}/Data/Gold/{username}.duckdb')
# con.execute(f"""
#     CREATE TABLE IF NOT EXISTS meta AS 
#     SELECT * FROM read_csv_auto('{project_root}/Data/Gold/{username}_meta_gold.csv');
# """)
# print("="*50)
# print("DuckDB Database Metadata Table Complete")
# print("="*50)
# print()
# con.execute(f"""
#     CREATE TABLE IF NOT EXISTS moves AS
#     SELECT * FROM read_csv_auto('{project_root}/Data/Gold/{username}_moves_gold.csv');
# """)
# print("="*50)
# print("DuckDB Database Moves Table Complete")
# print("="*50)
# print()
# con.close()