import pandas as pd

def load_id_to_name_mapping():
    """
    Loads and prepares a card mapping dictnary (ID → GP WR).
    io
    Returns:
        dict: A dictionary mapping card IDs to GP WR.
    """
    cards = pd.read_csv(r'C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\data\cards_data\cards.csv')
    name_mapping = cards[['id', 'name']]
    return name_mapping.set_index('id')['name'].to_dict()