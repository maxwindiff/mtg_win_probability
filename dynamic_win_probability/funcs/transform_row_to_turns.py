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
    
    for turn in range(1, row['num_turns'] + 1):  # Iterate through the turns
        # Create a dictionary to hold features for the current turn
        turn_data = {
            'game_id': row['draft_id'],  # Unique identifier for the game
            'turn': turn,
            'on_play': row.get('on_play', None),
            'won': row.get('won', None),  # Target variable
        }
        try:
            turn_data['unique_id'] = row['unique_id']
        except:
            pass
        
        # Add game state metrics for user and opponent dynamically
        for player in ['user', 'oppo']:
            # Handle cards in hand
            if player == "user":
                cards_in_hand_str = row.get(f'{player}_turn_{turn}_eot_{player}_cards_in_hand', None)
              
                exploded_cards = explode_cards(cards_in_hand_str, max_cards=max_cards)
              
                card_columns = generate_card_columns(exploded_cards, f'{player}_hand')
                
                turn_data.update(card_columns)
           
             
            if player == "oppo":
                turn_data[f'{player}_cards_in_hand'] = row.get(f'{player}_turn_{turn}_eot_{player}_cards_in_hand', None)

            # Handle lands
            land_values = row.get(f'{player}_turn_{turn}_eot_{player}_lands_in_play', None)
            turn_data[f'{player}_lands_in_play'] = count_player_lands(land_values)
            
            # Handle creatures
            creatures_in_play_str = row.get(f'{player}_turn_{turn}_eot_{player}_creatures_in_play', None)
            exploded_creatures = explode_cards(creatures_in_play_str, max_cards=max_cards)
            creature_columns = generate_card_columns(exploded_creatures, f'{player}_creatures')
            turn_data.update(creature_columns)
            
            # Handle non-creatures
            non_creatures_in_play_str = row.get(f'{player}_turn_{turn}_eot_{player}_non_creatures_in_play', None)
            exploded_non_creatures = explode_cards(non_creatures_in_play_str, max_cards=max_cards)
            non_creature_columns = generate_card_columns(exploded_non_creatures, f'{player}_non_creatures')
            turn_data.update(non_creature_columns)
            
            # Handle life
            turn_data[f'{player}_life'] = row.get(f'{player}_turn_{turn}_eot_{player}_life', None)
          
        # Append the turn data dictionary to the list
        turns.append(turn_data)

    # Convert the list of dictionaries into a DataFrame
    turn_df = pd.DataFrame(turns)

    # Apply ID-to-winrate mapping for relevant columns
    for prefix in ['user_hand', 'oppo_hand', 'user_creatures', 'oppo_creatures', 'user_non_creatures', 'oppo_non_creatures']:
        if display:
            
            turn_df = apply_winrate_mapping(turn_df, id_to_name_mapping,  column_prefix = prefix, max_cards=max_cards, dynamic_winrate = False)
        if dynamic_winrate:
        
                if 'creature' in prefix:  # becaue the dynamic winrate mapping is only for on board stuff right now creature and non_creature
                    # print(f'applying dynamic winrate mapping for {prefix}')
                    turn_df = apply_winrate_mapping(turn_df, id_to_wr_mapping = dynamic_id_to_wr_mapping, static_mapping = id_to_wr_mapping, column_prefix = prefix, max_cards=max_cards, dynamic_winrate = dynamic_winrate)
                else:
                    turn_df = apply_winrate_mapping(turn_df, id_to_wr_mapping = id_to_wr_mapping,static_mapping = id_to_wr_mapping, column_prefix = prefix, max_cards=max_cards, dynamic_winrate = False)
        else:
            turn_df = apply_winrate_mapping(turn_df, id_to_wr_mapping= id_to_wr_mapping, static_mapping = id_to_wr_mapping, column_prefix = prefix, max_cards=max_cards, dynamic_winrate = False)
    
    return turn_df
