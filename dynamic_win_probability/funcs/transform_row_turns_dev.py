import pandas as pd
from typing import List
from explode_cards import explode_cards
from generate_card_columns import generate_card_columns
from count_player_lands import count_player_lands
from apply_winrate_mapping import apply_winrate_mapping
from load_id_to_wr_mapping import load_id_to_wr_mapping
from load_id_to_name_mapping import load_id_to_name_mapping
from load_id_to_wr_turn_mapping import load_id_to_wr_turn_mapping


def transform_row_to_turns(row, id_to_wr_mapping = None, max_cards=20, dynamic_winrate = False, display = False):
    """
    Transforms a single game row into multiple rows, one for each turn,
    and replaces card IDs with GP WR values.

    Parameters:
    row (pd.Series): A single row from the original dataset.
    id_to_wr_mapping (dict): A dictionary mapping card IDs to GP WR values.
    max_cards (int): Maximum number of slots for cards in hand or on the board.

    Returns:
    pd.DataFrame: A DataFrame where each row represents a turn with GP WR values.
    """
    # print('inside transform_row_to_turns')
    if dynamic_winrate:
        # print('dynamic_winrate is true')
        dynamic_id_to_wr_mapping = load_id_to_wr_turn_mapping()
        id_to_wr_mapping = load_id_to_wr_mapping()
    else:
        if id_to_wr_mapping is None:
            id_to_wr_mapping = load_id_to_wr_mapping()
        if display:
            id_to_name_mapping = load_id_to_name_mapping()

    turns = []  # Use a list to collect all turn data dictionaries

    