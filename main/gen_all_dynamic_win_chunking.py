import os
import sys
import time
import pandas as pd
import hashlib


current_dir = os.getcwd()
funcs_dir = os.path.join(current_dir, 'funcs')

if funcs_dir not in sys.path:
    sys.path.append(funcs_dir)

# Import required functions
from get_input_columns import get_input_columns
from transform_replay_data import transform_replay_data
from load_id_to_wr_turn_mapping import load_id_to_wr_turn_mapping

# Define paths
input_file_folder_path = r'./data/raw_csv'
save_file_path = r"./data/processed_csv/dynamic_winrate_by_turn.csv"

# Function to generate a unique ID for rows
def generate_unique_id(row):
    unique_string = f"{row['draft_id']}-{row['opening_hand']}"
    return hashlib.md5(unique_string.encode()).hexdigest()

# Function to add a unique identifier column
def add_unique_identifier(data):
    data['unique_id'] = data.apply(generate_unique_id, axis=1)
    return data

# Function to process data in chunks
def process_data_with_chunking(input_file, transform_function, save_path, mapping, dynamic_winrate=True, nrows=100000, chunk_size=5000):
    print(f"Loading data from {input_file}...")
    data = pd.read_csv(input_file, nrows=nrows)
    
    print("Adding unique identifiers to the data...")
    data = add_unique_identifier(data)

    # Load processed unique IDs if save file exists
    processed_ids = set()
    if os.path.exists(save_file_path):
        print(f"Save file found at {save_file_path}. Skipping already processed rows...")
        processed_ids = set(pd.read_csv(save_file_path, usecols=['unique_id'])['unique_id'])
    else:
        print("No save file found. Starting fresh.")

    # Filter unprocessed rows
    unprocessed_data = data[~data['unique_id'].isin(processed_ids)]
    total_rows = len(unprocessed_data)
    print(f"Total rows to process: {total_rows}")

    # Process in chunks
    for start_idx in range(0, total_rows, chunk_size):
        end_idx = min(start_idx + chunk_size, total_rows)
        print(f"\nProcessing rows {start_idx + 1} to {end_idx}...")
        chunk = unprocessed_data.iloc[start_idx:end_idx]

        output_dynamic = transform_function(chunk, mapping, dynamic_winrate=dynamic_winrate)

        # Append or create the save file
        if os.path.exists(save_file_path):
            output_dynamic.to_csv(save_file_path, mode='a', index=False, header=False)
        else:
            output_dynamic.to_csv(save_file_path, mode='w', index=False, header=True)

        print(f"Chunk processed and saved.")

# Main execution
if __name__ == "__main__":
    print("Setting up environment...")
    print(f"Current working directory: {current_dir}")
    print(f"Functions directory: {funcs_dir}")

    # Load the mapping
    print("Loading mapping...")
    load_id_to_wr_turn_mapping = load_id_to_wr_turn_mapping()

    # Process each CSV file
    for file in os.listdir(input_file_folder_path):
        if file.endswith(".csv.gz"):
            input_file_path = os.path.join(input_file_folder_path, file)

            print(f"Processing file: {file}...")

            process_data_with_chunking(
                input_file=input_file_path,
                transform_function=transform_replay_data,
                save_path=save_file_path,
                mapping=load_id_to_wr_turn_mapping,
                dynamic_winrate=True,
                nrows=100000,
                chunk_size=10000
            )

    print("\nAll files processed.")
