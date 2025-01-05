def generate_card_columns(exploded_cards, prefix):
    """
    Generate a dictionary for card columns with appropriate names.
    
    Parameters:
        exploded_cards (list): A list of card values (e.g., from `explode_cards`).
        prefix (str): The prefix for the column names (e.g., 'user_hand').
    
    Returns:
        dict: A dictionary with keys like 'user_hand_1', 'user_hand_2', ..., and corresponding card values.
    """
    return {f'{prefix}_{i+1}': exploded_cards[i] for i in range(len(exploded_cards))}

