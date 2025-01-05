import pandas as pd
def count_player_lands(player_land_value):
    """
    count the number of '|' in the string return that number + 1. If the value is NaN return 0

    """
    player_land_value = str(player_land_value)
    
    if pd.isna(player_land_value):
        return 0

    return player_land_value.count('|') + 1