import pandas as pd
import numpy as np

def sort_zone_by_winrate(df, prefixes, exclude_columns=None):
    """
    Sorts columns within zones (based on prefixes) by descending winrate for each row,
    handling NaN values appropriately. Columns not in any zone are appended to the front.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing zone data.
        prefixes (list of str): List of prefixes to identify zones (e.g., ['user_hand_', 'oppo_hand_']).
        exclude_columns (list of str): Columns to exclude from sorting (e.g., ['user_lands_in_play']).

    Returns:
        pd.DataFrame: DataFrame with sorted columns within each zone and other columns in front.
    """
    sorted_df = df.copy()  # Work on a copy to preserve the original DataFrame
    exclude_columns = exclude_columns or []  # Default to empty list if not provided

    # Identify zone columns and other columns
    zone_columns = []
    for prefix in prefixes:
        zone_columns.extend([col for col in df.columns if col.startswith(prefix) and col not in exclude_columns])
    other_columns = [col for col in df.columns if col not in zone_columns and col not in exclude_columns]

    # Sort values within each zone
    for prefix in prefixes:
        current_zone_columns = [col for col in zone_columns if col.startswith(prefix)]
        
        if current_zone_columns:
            sorted_zone_values = []
            for _, row in df[current_zone_columns].iterrows():
                row_values = row.dropna().sort_values(ascending=False).tolist()  # Sort non-NaN values
                row_values.extend([np.nan] * (len(current_zone_columns) - len(row_values)))  # Pad with NaN
                sorted_zone_values.append(row_values)
            
            # Create a DataFrame from the sorted values and assign back
            sorted_zone_df = pd.DataFrame(sorted_zone_values, columns=current_zone_columns, index=df.index)
            sorted_df[current_zone_columns] = sorted_zone_df

    # Reorder columns: Other columns first, then zone columns
    reordered_columns = other_columns + zone_columns
    sorted_df = sorted_df[reordered_columns]

    return sorted_df

if __name__ == '__main__':
    

    # Load the data
    print('hello world')
    data = pd.read_csv(r"C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\data\replay_data\transformed_replay_data_win_probability\dynamic_win_probability_50k.csv", nrows=50)
    
    # Apply sorting while excluding specific columns
    sorted_data = sort_zone_by_winrate(
        data,
        prefixes=[
            'user_hand_', 'oppo_hand_',
            'user_creatures_', 'oppo_creatures_',
            'user_non_creatures_', 'oppo_non_creatures_'
        ],
        exclude_columns=['user_lands_in_play', 'oppo_lands_in_play', 'turn', 'on_play']
    )
    
    # Save the sorted DataFrame as a CSV
    sorted_data.to_csv('test_sorted_corrected.csv', index=False)
