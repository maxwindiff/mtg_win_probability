
def get_card_columns(df, column_prefix, max_cards):
    """
    Identifies columns in the DataFrame corresponding to card slots (e.g., user_hand_1, user_hand_2, ...).
    
    Parameters:
        df (pd.DataFrame): The DataFrame to check for card columns.
        column_prefix (str): The prefix for the column names (e.g., 'user_hand').
        max_cards (int): The maximum number of card slots to check for.
    
    Returns:
        list: A list of column names that exist in the DataFrame matching the prefix and range.
    """
    
    return [f'{column_prefix}_{i}' for i in range(1, max_cards + 1) if f'{column_prefix}_{i}' in df.columns]
