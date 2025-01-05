import os
import sys
import time
import pandas as pd
import hashlib

# Set up the working directory
os.chdir(r"C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\dynamic_win_probability")
current_dir = os.getcwd()
funcs_dir = os.path.join(current_dir, 'funcs')

if funcs_dir not in sys.path:
    sys.path.append(funcs_dir)

# Import required functions from your project
from get_input_columns import get_input_columns
from transform_replay_data import transform_replay_data
from load_id_to_wr_turn_mapping import load_id_to_wr_turn_mapping

# Define paths
input_file_path = r'..\data\replay_data\replay_data_public.DSK.PremierDraft.csv'
save_file_path = r"C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\data\replay_data\transformed_replay_data_win_probability\dynamic_win_prob_chunked.csv"
nrows = 300000
def generate_unique_id(row):
    """
    Generates a unique ID for a row based on selected columns.
    """
    unique_string = f"{row['draft_id']}-{row['opening_hand']}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def add_unique_identifier(data):
    """
    Adds a unique identifier column to the DataFrame.
    """
    data['unique_id'] = data.apply(generate_unique_id, axis=1)
    return data

def process_data_with_chunking(input_file, transform_function, save_path, mapping, dynamic_winrate=True,nrows = 100000, chunk_size=5000):
    """
    Processes the data in chunks based on unique IDs and saves the output incrementally.

    Parameters:
        input_file (str): Path to the input data file.
        transform_function (function): The transformation function to apply.
        save_path (str): The path to save the transformed data.
        mapping (any): Mapping data required for the transformation.
        dynamic_winrate (bool): Whether to calculate dynamic winrate.
        chunk_size (int): Number of rows per chunk.
    """
    # Load the input data
    print(f"Loading data from {input_file}...")
    data = pd.read_csv(input_file, nrows = nrows)

    # Add unique identifiers
    print("Adding unique identifiers to the data...")
    data = add_unique_identifier(data)

    # Determine the starting point
    if os.path.exists(save_path):
        print(f"Save file found at {save_path}. Resuming from last processed chunk...")
        processed_ids = set(pd.read_csv(save_path, usecols=['unique_id'])['unique_id'])  # Get processed unique IDs
    else:
        print(f"No save file found. Starting from the beginning...")
        processed_ids = set()

    # Filter out already processed rows
    unprocessed_data = data[~data['unique_id'].isin(processed_ids)]
    total_rows = len(unprocessed_data)
    print(f"Total rows to process: {total_rows}")

    # Start processing
    start_time = time.time()
    for start_idx in range(0, total_rows, chunk_size):
        end_idx = min(start_idx + chunk_size, total_rows)
        print(f"\nProcessing rows {start_idx + 1} to {end_idx}...")

        # Extract chunk
        chunk = unprocessed_data.iloc[start_idx:end_idx]

        # Start chunk timer
        chunk_start_time = time.time()

        # Execute the transformation function
        output_dynamic = transform_function(chunk, mapping, dynamic_winrate=dynamic_winrate)

        # Append or create the CSV
        if os.path.exists(save_path):
            output_dynamic.to_csv(save_path, mode='a', index=False, header=False)
        else:
            output_dynamic.to_csv(save_path, mode='w', index=False, header=True)

        # Timing and progress
        chunk_elapsed_time = time.time() - chunk_start_time
        rows_processed = end_idx
        rows_remaining = total_rows - rows_processed
        est_time_remaining = (chunk_elapsed_time / chunk_size) * (rows_remaining / chunk_size) if rows_processed > 0 else 0

        print(f"Chunk processed in {chunk_elapsed_time:.2f} seconds.")
        print(f"Estimated time remaining: {est_time_remaining / 60:.2f} minutes.")

    print("\nProcessing completed. All chunks have been saved.")

# Main execution
if __name__ == "__main__":
    os.chdir(r"C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\dynamic_win_probability")

    print("Setting up environment...")
    print(f"Current working directory: {current_dir}")
    print(f"Functions directory: {funcs_dir}")

    print("Loading mapping...")
    load_id_to_wr_turn_mapping = load_id_to_wr_turn_mapping()  # Load the mapping

    print("Starting chunk processing...")
    process_data_with_chunking(
        input_file=input_file_path,
        transform_function=transform_replay_data,
        save_path=save_file_path,
        mapping=load_id_to_wr_turn_mapping,
        dynamic_winrate=True,
        nrows = nrows,
        chunk_size=10000  # Adjust as needed
    )
