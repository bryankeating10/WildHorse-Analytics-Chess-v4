"""
Stockfish evaluation using the stockfish Python package.

Usage:
    from Utils.add_eval import add_eval
    eval_series = add_eval(fen_series, depth=15)
"""

import pandas as pd
from stockfish import Stockfish
import chess

# Stockfish path
STOCK_PATH = r"C:\Tools\stockfish\stockfish-windows-x86-64-avx2.exe"


def is_valid_fen(fen: str) -> bool:
    """Check if FEN is valid and represents a legal position."""
    try:
        board = chess.Board(fen)
        return board.is_valid()
    except:
        return False


def add_eval(fen_series: pd.Series, depth: int = 15) -> pd.Series:
    """
    Add Stockfish evaluation to a Series of FENs.

    Parameters:
    -----------
    fen_series : pd.Series
        index = game_id
        values = fen strings
    depth : int
        Stockfish depth (default: 15)

    Returns:
    --------
    pd.Series
        index = game_id
        values = evaluations
    """
    stockfish = Stockfish(path=STOCK_PATH, depth=depth)

    evals = []
    invalid_count = 0
    total = len(fen_series)

    for i, fen in fen_series.items():

        if not is_valid_fen(fen):
            print(f"Invalid FEN at index {i}: {fen[:50]}...")
            evals.append(None)
            invalid_count += 1
            continue

        try:
            stockfish.set_fen_position(fen)
            evaluation = stockfish.get_evaluation()

            if evaluation["type"] == "cp":
                value = evaluation["value"] / 100.0
            else:
                value = f"M{evaluation['value']}"

            evals.append(value)

        except Exception as e:
            print(f"Error at index {i}: {e}")
            evals.append(None)

    print(f"\nCompleted: {total} positions")
    print(f"Invalid FENs: {invalid_count}")

    return pd.Series(evals, index=fen_series.index, name="eval")