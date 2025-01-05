import numpy as np
def explode_cards(card_string, max_cards=20):
    """
    Explodes a delimited card string into a fixed-length list with NaN for missing values.
    
    Parameters:
        card_string (str): The string containing delimited card numbers.
        max_cards (int): The maximum number of card slots to return.
        
    Returns:
        list: A list of length `max_cards` containing card numbers or NaN.
    """
    if not isinstance(card_string, str) or not card_string:
        return [np.nan] * max_cards  # Handle empty or non-string input
    
    cards = card_string.split('|')  # Split the string into a list
    exploded = cards[:max_cards] + [np.nan] * (max_cards - len(cards))  # Pad with NaN if fewer than max_cards
    return exploded