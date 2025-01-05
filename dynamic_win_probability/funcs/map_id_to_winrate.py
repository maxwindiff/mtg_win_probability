import numpy as np
from load_id_to_wr_mapping import load_id_to_wr_mapping
def map_id_to_winrate(card_id, id_to_wr_mapping,static_mapping, turn = None, recalc_winrates = None, by_turn = False,  dynamic_winrate = False):

    """
    Maps a single card ID to its winrate using the provided dictionary.
    
    Parameters:
        value (int): The card ID to map.
        id_to_wr_mapping (dict): A dictionary mapping card IDs to winrates.
    
    Returns:
        float: The winrate of the card ID, or NaN if not found.
    """
    # print(f'mapping id {card_id} to winrate')
    if dynamic_winrate:
        # print('winrate is set to dynamic')
        card_id_key = card_id + '_' + str(turn)
        mapped_wr = id_to_wr_mapping.get(card_id_key, np.nan)
        # print('key:', card_id_key, 'mapped_wr:', mapped_wr)
        if np.isnan(mapped_wr):
            # print('key not found for dynamic winrate, using static winrate')
           
            # print('using card_id as key:', card_id)
            
            mapped_wr = static_mapping.get(int(card_id), np.nan)
            # print('returning value for dynamic winrate (replaced with static):', mapped_wr)
        # print('returning value for dynamic winrate:', mapped_wr)
        return mapped_wr

    
    else:
        card_id = int(card_id)
        # print('winrate is set to static')
        wr_mapping = id_to_wr_mapping.get(card_id, np.nan)
        # print(f'returning value for static winrate: {wr_mapping}')
        if wr_mapping is np.nan:
            # print('trying as a string')
            card_id = str(card_id)
            wr_mapping = static_mapping.get(card_id, np.nan)
            # print(f'returning value for static winrate (replaced with static): {wr_mapping}')
        return wr_mapping
    # return id_to_wr_mapping.get(card_id, np.nan)
