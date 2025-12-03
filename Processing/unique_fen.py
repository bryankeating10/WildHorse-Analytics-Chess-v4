"""
Docstring for Processing.unique_fen

This module provides functions for evaluating unique FENs so 
Stockfish is not run on duplicate positions.
"""

import pandas as pd
import numpy as np


def unique_fens(moves_df):
    """
    Extract unique FEN strings from a moves dataframe.
    
    Parameters:
    -----------
    moves_df : pandas.DataFrame
        DataFrame containing a 'fen' column with FEN strings
        
    Returns:
    --------
    pandas.Series
        Series indexed by unique FEN strings, with NaN values as placeholders
        for evaluations to be filled in later
    """
    # Extract unique FENs
    unique_fen_values = moves_df['fen'].unique()
    
    # Create Series indexed by FEN, initialized with NaN
    unique_fen_series = pd.Series(
        data=np.nan,
        index=unique_fen_values,
        name='evaluation'
    )
    
    return unique_fen_series


def repopulate_unique_evals(moves_df, unique_fen_series):
    """
    Map evaluations from unique FEN series back to the original moves dataframe.
    
    Parameters:
    -----------
    moves_df : pandas.DataFrame
        Original DataFrame containing a 'fen' column
    unique_fen_series : pandas.Series
        Series indexed by FEN strings, containing evaluation data
        
    Returns:
    --------
    pandas.DataFrame
        The moves_df with a new 'evaluation' column containing the mapped evaluations
    """
    # Map evaluations from the unique_fen_series to the moves_df
    # This preserves the original row order
    moves_df['evaluation'] = moves_df['fen'].map(unique_fen_series)
    
    return moves_df