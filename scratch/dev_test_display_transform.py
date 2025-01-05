# %%
import pandas as pd
import os 
import sys

# %%
current_dir = os.getcwd()
funcs_dir = os.path.join(current_dir, 'funcs')
if funcs_dir not in sys.path:
    sys.path.append(funcs_dir)

# %%
from funcs.transform_row_to_turns import transform_row_to_turns
from funcs.load_id_to_name_mapping import load_id_to_name_mapping
from funcs.load_id_to_wr_mappings import load_id_to_wr_mappings
from funcs.display_game_state import display_game_state

# %%
load_id_to_wr_mappings()

# %%
data = pd.read_csv('../data/replay_data/replay_data_public.DSK.PremierDraft.csv', nrows = 10)

# %%
all_turns = []
    
# Iterate through each row in the data
for idx, row in data.iterrows():
    # Transform the row into a DataFrame of turns
    turn_df = transform_row_to_turns(row, display = True,  max_cards=10)
    
    # Append the DataFrame to the list
    all_turns.append(turn_df)
    all_turns_df = pd.concat(all_turns, ignore_index=True)
    

# %%

def clear_screen():
    """
    Clears the terminal screen.
    Works on Windows, macOS, and Linux.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def watch_game(all_turns):
    """
    Displays game states sequentially, clearing the screen between states.
    - all_turns: list of game states (DataFrames or Series).
    """
    if not all_turns:
        print("No game states to display.")
        return

    for idx, turn in enumerate(all_turns):
        clear_screen()  # Clear the screen
        print(f"Displaying game state {idx + 1} of {len(all_turns)}:\n")
        display_game_state(turn)  # Display the current game state
        input("\nPress Enter to continue...")  # Wait for user to press Enter

# %%
import os

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Iterate through all rows in all_turns_df
for index, row in all_turns_df.iterrows():
    clear_screen()  # Clear the screen
    print(f"Displaying game state {index + 1} of {len(all_turns_df)}:\n")
    display_game_state(row)  # Pass the row as a Series
    input("\nPress Enter to continue...")










