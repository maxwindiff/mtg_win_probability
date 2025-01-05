import pandas as pd
import numpy as np
import re

from get_card_columns import get_card_columns
from map_id_to_winrate import map_id_to_winrate


def apply_winrate_mapping(df, id_to_wr_mapping, static_mapping,  column_prefix, max_cards, dynamic_winrate = False):
    """
    Applies map_id_to_winrate to the specified card columns in the DataFrame.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the card ID columns.
        id_to_wr_mapping (dict): A dictionary mapping card IDs to GP WR values.
        column_prefix (str): The prefix for the column names (e.g., 'user_hand').
        max_cards (int): The maximum number of card slots to check for.
    
    Returns:
        pd.DataFrame: The updated DataFrame with card IDs replaced by GP WR values.
    """
    # print('inside apply_winrate_mapping')
    cols = [col for col in df.columns.tolist() if 'creature' in col]
    # print('wokring on df', df[cols])
    card_columns = get_card_columns(df, column_prefix, max_cards)
    # for winrate_by_turn

    # for col in card columns:
    #     # extract the turn from the col name
    #     turn = int(col.split('_')[-1])
    #     # get the winrate for the card id by looking up the id where the turn is
    for col in card_columns:
        if dynamic_winrate:
            # print(f'inside apply_winrate_mapping, working on col {col}')
            turn = int(re.search(r'\d+', col).group())
            # print('working on turn', turn)
            df[col] = df[col].apply(lambda x: map_id_to_winrate(x, id_to_wr_mapping, static_mapping, turn = turn, dynamic_winrate = True) if pd.notnull(x) else np.nan)          
         
        else:
            df[col] = df[col].apply(lambda x: map_id_to_winrate(x, id_to_wr_mapping, static_mapping) if pd.notnull(x) else np.nan)
    # print('returning df from apply_winrate_mapping', df)
    # input('press enter to continue')
    return df