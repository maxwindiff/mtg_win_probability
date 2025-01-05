import os
import sys
import json
import pandas as pd

sys.path.append('funcs')
from calc_turn_based_win_rate import calc_turn_based_win_rate

def process_chunk(chunk, output_dict):
    """Process a single chunk and update the output dictionary."""
    temp_dict = calc_turn_based_win_rate(chunk, baseline=1)
    for key, vals in temp_dict.items():
        if key in output_dict:
            for turn in vals:
                if turn not in output_dict[key]:
                    output_dict[key][turn] = vals[turn]
                else:
                    wr = vals[turn]['wr']
                    total = vals[turn]['total']
                    current_wr = output_dict[key][turn]['wr']
                    current_total = output_dict[key][turn]['total']

                    new_total = current_total + total
                    new_wr = (current_wr * current_total + wr * total) / new_total
                    output_dict[key][turn] = {'wr': new_wr, 'total': new_total}
        else:
            output_dict[key] = vals

def save_progress(output_dict, progress_file):
    """Save the current output_dict and progress to disk."""
    with open(progress_file, 'w') as f:
        json.dump(output_dict, f)
    print(f"Progress saved to {progress_file}")

if __name__ == "__main__":
    raw_data_path = r"data/raw_csv"
    output_dict = {}
    progress_file = 'data/card_wr_by_turn_dict/card_wr_by_turn_total.json'
    completed_files_file = 'data/card_wr_by_turn_dict/completed_files.json'
    
    # Load previous progress if it exists
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            output_dict = json.load(f)
        print(f"Loaded previous progress from {progress_file}")
    
    completed_files = []
    if os.path.exists(completed_files_file):
        with open(completed_files_file, 'r') as f:
            completed_files = json.load(f)
        print(f"Loaded completed files list from {completed_files_file}")

    filenames = os.listdir(raw_data_path)
    
    for file in filenames:
        if file in completed_files:
            print(f"Skipping completed file: {file}")
            continue
        
        file_path = os.path.join(raw_data_path, file)
        print(f"Processing file: {file}")
        
        # Process file in chunks
        for chunk in pd.read_csv(file_path, chunksize=100000):
            process_chunk(chunk, output_dict)
            print('processed chunk')
        
        # Mark file as completed
        completed_files.append(file)
        
        # Save progress periodically
        save_progress(output_dict, progress_file)
        with open(completed_files_file, 'w') as f:
            json.dump(completed_files, f)

    print("All files processed.")
