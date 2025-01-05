import pandas as pd
from typing import List
from explode_cards import explode_cards
from generate_card_columns import generate_card_columns
from count_player_lands import count_player_lands
from apply_winrate_mapping import apply_winrate_mapping
from load_id_to_wr_mapping import load_id_to_wr_mapping
from load_id_to_name_mapping import load_id_to_name_mapping
from load_id_to_wr_turn_mapping import load_id_to_wr_turn_mapping

def gen_single_turn_dict(row, player, turn, max_cards = 20):

    

    for turn_owner in ['user', 'oppo']:
        turn_dict = {}
        turn_dict[turn] = {}
        base_turn_data = {
        'game_id': row['draft_id'],
        'turn': turn,
        'on_play': row.get('on_play', None),
        'won': row.get('won', None),
    }
        
        for player in ['user', 'oppo']:
            # handle cards in hand
            if player == "user":
                cards_in_hand_str = row.get(f'{turn_owner}_turn_{turn}_eot_{player}_cards_in_hand', None)
                exploded_cards = explode_cards(cards_in_hand_str, max_cards=max_cards)
                card_columns = generate_card_columns(exploded_cards, f'{player}_hand')
                base_turn_data.update(card_columns)
            if player == "oppo":
                base_turn_data[f'{player}_cards_in_hand'] = row.get(f'{player}_turn_{turn}_eot_{player}_cards_in_hand', None)
                  # Handle lands
            land_values = row.get(f'{turn_owner}_turn_{turn}_eot_{player}_lands_in_play', None)
            base_turn_data[f'{player}_lands_in_play'] = count_player_lands(land_values)
            
            if player == "user":
                user_turn =base_turn_data
            if player == "oppo":
                oppo_turn = base_turn_data
        
        turn_dict[turn]['user'] = user_turn
        turn_dict[turn]['oppo'] = oppo_turn

        return turn_dict





    


