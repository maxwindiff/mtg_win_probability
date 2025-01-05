import pandas as pd
from collections import defaultdict, Counter
import numpy as np
import re
import json

def calc_turn_based_win_rate(data, baseline=None):
    """
    Calculate the win rate of each card played on each turn in the game from a DataFrame.

    Args:
    data: DataFrame, chunk of raw data
    baseline: int, minimum number of samples to calculate win rate

    Returns:
    dict: A dictionary containing turn-based win rates for each card.
    """
    card_data = pd.read_csv("./data/cards.csv")
    card_name_map = dict(zip(card_data['id'].astype(str), card_data['name']))
    
    # Initialize a dictionary to store card stats
    card_stats = defaultdict(lambda: defaultdict(Counter))
    
    # Identify relevant columns
    turn_columns = [col for col in data.columns if "turn" in col and "in_play" in col and 'land' not in col]
    
    # Convert all 'nan' strings to np.nan
    data = data.replace('nan', np.nan)
    
    # Iterate through each row of the dataset
    for _, row in data.iterrows():
        for col in turn_columns:
            turn = int(col.split('_')[2])  # Turn number from column name
            
            # Skip if contains NaN
            if pd.isna(row[col]):
                continue
            
            # Get card IDs as a list
            cards = str(row[col]).split('|')
            cards = [card.split('.')[0] for card in cards]

            # Determine card owner
            regex = r'(?<=eot_)[^_]+'
            card_owner = re.search(regex, col).group(0)
            
            # Flip win for opponent's cards
            won = not row['won'] if card_owner == 'oppo' else row['won']
            
            for card in cards:
                card_stats[card][turn][won] += 1
    
    # Calculate win rates
    win_rates = calculate_win_rate(card_stats, baseline=baseline)
    return win_rates

def calculate_win_rate(card_stats, baseline=100):
    """
    Calculate win rates from card stats.

    Args:
    card_stats: dict
    baseline: int, minimum number of samples to calculate win rate

    Returns:
    dict: Win rates and totals for each card and turn.
    """
    win_rates = {}
    for card, turns in card_stats.items():
        win_rates[card] = {}
        for turn, won in turns.items():
            total = won[True] + won[False]
            
            if total >= baseline:
                wr = won[True] / total
            else:
                wr = None  # If below baseline, win rate is not calculated
            
            # Store both 'wr' and 'total' in a nested dictionary
            win_rates[card][turn] = {'wr': wr, 'total': total}
    
    return win_rates

def process_large_file(file_path, chunk_size=100000, baseline=100):
    """
    Process a large CSV file in chunks and calculate turn-based win rates.

    Args:
    file_path: str, path to the CSV file
    chunk_size: int, number of rows per chunk
    baseline: int, minimum number of samples to calculate win rate

    Returns:
    dict: Combined win rates from all chunks.
    """
    output_dict = defaultdict(lambda: defaultdict(lambda: {'wr': 0, 'total': 0}))

    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        temp_dict = calc_turn_based_win_rate(chunk, baseline=baseline)
        for card, turns in temp_dict.items():
            for turn, data in turns.items():
                if turn not in output_dict[card]:
                    output_dict[card][turn] = data
                else:
                    # Combine win rate and total for overlapping turns
                    current_data = output_dict[card][turn]
                    new_total = current_data['total'] + data['total']
                    new_wr = (
                        (current_data['wr'] * current_data['total']) +
                        (data['wr'] * data['total'])
                    ) / new_total
                    output_dict[card][turn] = {'wr': new_wr, 'total': new_total}
    
    return output_dict

if __name__ == '__main__':
    raw_data_path = r"C:\Users\jwright\Documents\GitHub\sevLandsPublicData\data\raw_csv\replay_data_public.LTR.PremierDraft.csv.gz"
    output_path = "temp/turn_based_win_rate.json"
    
    # Process the large file in chunks
    result_dict = process_large_file(raw_data_path, chunk_size=1000, baseline=1)
    print('processed chunk')
    # Save to a JSON file
    with open(output_path, 'w') as f:
        json.dump(result_dict, f)
    
    print(f"Win rate data saved to {output_path}")
