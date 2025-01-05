## MTG Win Probability

This project is created from public data on [17Lands](https://www.17lands.com/) and converts it from a **game-per-row format** to a **turn-per-row format** while retaining critical game information such as `won`, `on_play`, and more. The processed data can then be used to train machine learning models to estimate win probability based on the board state and cards in hand.

### Key Components

#### 1. Main Script
The primary entry point for processing data is:
```
main/gen_all_dynamic_win_chunking.py
```
This script handles the processing workflow, but note that it runs slowly in its current form.

#### 2. Main Processing Function
```
funcs/transform_replay_data
```
This function is the core of the data transformation process. It uses a card ID-to-win-rate mapping to replace card IDs in the data with their corresponding win rates for a given turn. This transformation reduces data sparsity and helps generalize the model to unseen cards in training and new cards in new sets. 

#### 3. Win Rate Mapping
The function relies on two types of win rate mappings:
- **Dynamic Win Rates**: Calculated using the script:
  ```
  generate_win_rate_dict/gen_all_turn_based_wr.py
  ```
- **Static Win Rates**: Pre-compiled data sourced directly from the 17Lands website.


## data to add

replays from https://www.17lands.com/public_datasets can be downloaded and placed in data/raw_csv to run the main function. 


