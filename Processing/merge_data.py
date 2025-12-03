"""
Merge metadata and moves dataframes.

Usage:
    from Utils.merge_data import merge_data
    merged_df = merge_data(meta_df, moves_df)
"""

import pandas as pd


def merge_data(meta_df: pd.DataFrame, moves_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge metadata and moves dataframes on game_id.
    
    Creates a long dataframe where each move row gets the metadata from its game.
    
    Parameters:
    -----------
    meta_df : pd.DataFrame
        Metadata dataframe with one row per game (must contain 'game_id')
    moves_df : pd.DataFrame
        Moves dataframe with many rows per game (must contain 'game_id')
        
    Returns:
    --------
    pd.DataFrame
        Merged long dataframe with metadata columns added to each move row
    """
    merged_df = moves_df.merge(meta_df, on='game_id', how='left')
    
    print(f"Merged {len(meta_df)} games with {len(moves_df)} moves into game dataframe")
    
    return merged_df