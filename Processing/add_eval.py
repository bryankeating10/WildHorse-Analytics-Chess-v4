"""
Stockfish evaluation using the stockfish Python package.

Usage:
    from Utils.add_eval import add_eval, add_eval_to_series
    
    # For unique FEN series (recommended for large datasets):
    unique_fen_series = add_eval_to_series(unique_fen_series, depth=15)
    
    # For direct dataframe evaluation (original behavior):
    df_with_evals = add_eval(move_df, depth=15)
"""

import pandas as pd
from stockfish import Stockfish
import chess

# Stockfish path
STOCK_PATH = r"C:\Tools\stockfish\stockfish-windows-x86-64-avx2.exe"


def is_valid_fen(fen: str) -> bool:
    """Check if FEN is valid and represents a legal position (including Chess960)."""
    try:
        # Try standard chess first
        board = chess.Board(fen)
        if board.is_valid():
            return True
    except:
        pass
    
    try:
        # If standard fails, try Chess960
        board = chess.Board(fen, chess960=True)
        return board.is_valid()
    except:
        return False


def add_eval_to_series(unique_fen_series: pd.Series, depth: int = 15) -> pd.Series:
    """
    Add Stockfish evaluation to a unique FEN Series.
    
    This is the recommended approach for large datasets with duplicate FENs,
    as it only evaluates each unique position once.

    Parameters:
    -----------
    unique_fen_series : pd.Series
        Series indexed by unique FEN strings, with NaN values as placeholders
    depth : int
        Analysis depth (default: 15)

    Returns:
    --------
    pd.Series
        Series with FEN index and evaluation values
    """
    # Initialize Stockfish and accept Chess960 positions
    stockfish = Stockfish(path=STOCK_PATH, depth=depth)
    stockfish.update_engine_parameters({"UCI_Chess960": True})
    
    total = len(unique_fen_series)
    invalid_count = 0
    evaluated_count = 0
    
    print(f"Evaluating {total} unique positions at depth {depth}...")
    
    # Iterate through the index (FEN strings)
    for i, fen in enumerate(unique_fen_series.index):
        
        # Validate FEN first
        if not is_valid_fen(fen):
            print(f"Invalid FEN at position {i}: {fen[:50]}...")
            unique_fen_series.iloc[i] = None  # Or 0.0
            invalid_count += 1
            continue
        
        try:
            stockfish.set_fen_position(fen)
            evaluation = stockfish.get_evaluation()
            
            # Extract value
            if evaluation['type'] == 'cp':
                eval_value = evaluation['value'] / 100.0  # Convert centipawns
            else:  # mate
                eval_value = f"M{evaluation['value']}"
            
            unique_fen_series.iloc[i] = eval_value
            evaluated_count += 1
            
        except Exception as e:
            print(f"Error at position {i}: {e}")
            unique_fen_series.iloc[i] = None
        
        # Progress
        if (i + 1) % 50 == 0:
            print(f"Evaluated {i + 1}/{total} positions... ({invalid_count} invalid)")
    
    print(f"\nCompleted: {total} positions")
    print(f"Successfully evaluated: {evaluated_count}")
    print(f"Invalid FENs: {invalid_count}")
    
    return unique_fen_series


def add_eval(move_df: pd.DataFrame, depth: int = 15) -> pd.DataFrame:
    """
    Add Stockfish evaluation to moves DataFrame.
    
    NOTE: For large datasets with duplicate FENs, consider using the 
    unique_fens() → add_eval_to_series() → repopulate_unique_evals() 
    pipeline instead for better performance.

    Parameters:
    -----------
    move_df : pd.DataFrame
        DataFrame with 'fen' column
    depth : int
        Analysis depth (default: 15)

    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'eval' column
    """
    df = move_df.copy()
    
    # Initialize Stockfish
    stockfish = Stockfish(path=STOCK_PATH, depth=depth)
    
    evals = []
    total = len(df)
    invalid_count = 0
    
    for index, row in df.iterrows():
        fen = row['fen']
        
        # Validate FEN first
        if not is_valid_fen(fen):
            print(f"Invalid FEN at position {index}: {fen[:50]}...")
            evals.append(None)  # Or 0.0
            invalid_count += 1
            continue
        
        try:
            stockfish.set_fen_position(fen)
            evaluation = stockfish.get_evaluation()
            
            # Extract value
            if evaluation['type'] == 'cp':
                eval_value = evaluation['value'] / 100.0  # Convert centipawns
            else:  # mate
                eval_value = f"M{evaluation['value']}"
            
            evals.append(eval_value)
            
        except Exception as e:
            print(f"Error at position {index}: {e}")
            evals.append(None)
        
        # Progress
        if (index + 1) % 50 == 0:
            print(f"Evaluated {index + 1}/{total} positions... ({invalid_count} invalid)")
    
    df['eval'] = evals
    print(f"\nCompleted: {total} positions")
    print(f"Invalid FENs: {invalid_count}")
    
    return df