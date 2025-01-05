import pandas as pd

# def display_game_state(turn_row):
#     """
#     Displays an ASCII-style game state with card names inside boxes for both the opponent and user.
#     - turn_row: DataFrame, a single game state row
#     """
#     # Helper function to create a box for a card
#     def card_box(card_name):
#         return f"[{card_name:^5}]"  # Center-align the card name in the box

#     # Extract scalar values safely using .iloc[0]
#     turn = int(turn_row['turn'].iloc[0])
#     oppo_life = float(turn_row['oppo_life'].iloc[0])
#     user_life = float(turn_row['user_life'].iloc[0])
#     oppo_cards_in_hand = int(turn_row['oppo_cards_in_hand'].iloc[0])
#     oppo_lands_in_play = int(turn_row['oppo_lands_in_play'].iloc[0])
#     user_lands_in_play = int(turn_row['user_lands_in_play'].iloc[0])

#     # Opponent's life and cards
#     print(f"Turn {turn}")
#     print(f"Opponent Life: {oppo_life}")
#     print("Opponent Hand:")
#     print(" ".join([card_box("???") for _ in range(oppo_cards_in_hand)]))  # Hidden cards
#     print("Opponent Lands:")
#     print(" ".join([card_box("Land") for _ in range(oppo_lands_in_play)]))  # Opponent's lands

#     # Filter columns matching 'oppo_creature_<n>' and 'oppo_noncreature_<n>'
#     oppo_creature_columns = [col for col in turn_row.columns if 'oppo_creature' in col]
#     oppo_noncreature_columns = [col for col in turn_row.columns if 'oppo_noncreature' in col]

#     # Extract non-null creature and non-creature names
#     oppo_creatures = turn_row[oppo_creature_columns].iloc[0].dropna().values  # Filter out NaN
#     oppo_noncreatures = turn_row[oppo_noncreature_columns].iloc[0].dropna().values

#     # Format and display the opponent's board
#     oppo_creature_print = " ".join([card_box(card) for card in oppo_creatures])
#     oppo_noncreature_print = " ".join([card_box(card) for card in oppo_noncreatures])
#     oppo_in_play_row = f"{oppo_creature_print}  ||  {oppo_noncreature_print}"
#     print("Opponent Board:")
#     print(oppo_in_play_row)

#     print("\n" + "=" * 30 + "\n")  # Separator

#     user_creature_columns = [col for col in turn_row.columns if 'user_creature' in col]
#     user_noncreature_columns = [col for col in turn_row.columns if 'user_noncreature' in col]

#     user_creatures = turn_row[user_creature_columns].iloc[0].dropna().values  # Filter out NaN
#     user_noncreatures = turn_row[user_noncreature_columns].iloc[0].dropna().values

#     user_creature_print = " ".join([card_box(card) for card in user_creatures])
#     user_noncreature_print = " ".join([card_box(card) for card in user_noncreatures])
#     user_in_play_row = f"{user_creature_print}  ||  {user_noncreature_print}"

#     print(user_in_play_row)
#     print("User Board:")
 
    
#     user_lands = " ".join([card_box("Land") for _ in range(user_lands_in_play)])
#     print(user_lands)
#     print('User Lands:')
#     user_hand_columns = [col for col in turn_row.columns if 'user_hand' in col]
#     user_hand = turn_row[user_hand_columns].iloc[0].dropna().values
#     user_hand_print = " ".join([card_box(card) for card in user_hand])
#     print(user_hand_print)
#     print('User Hand:')
#     print(f"User Life: {user_life}")
#     # Filter columns matching 'user_creature_<n>' and 'user_noncreature_<n>'
#     user_creature_columns = [col for col in turn_row.columns if 'user_creature' in col]
#     user_noncreature_columns = [col for col in turn_row.columns if 'user_noncreature' in col]

#     # Extract non-null creature and non-creature names for the user
#     user_creatures = turn_row[user_creature_columns].iloc[0].dropna().values  # Filter out NaN
#     user_noncreatures = turn_row[user_noncreature_columns].iloc[0].dropna().values

#     # Format and display the user's board
#     user_creature_print = " ".join([card_box(card) for card in user_creatures])
#     user_noncreature_print = " ".join([card_box(card) for card in user_noncreatures])
    


def display_game_state(turn_row):
    """
    Displays an ASCII-style game state with card names inside boxes for both the opponent and user.
    - turn_row: Series, a single game state row
    """
    # Helper function to create a box for a card
    def card_box(card_name):
        return f"[{card_name:^5}]"  # Center-align the card name in the box

    # Extract scalar values safely directly from the Series
    if 'predict_proba' in turn_row.index:
        print('Predicted Win Probability:', turn_row['predict_proba'])
        print("\n" + "*" * 30 + "\n")  # Separator
    turn = int(turn_row['turn'])
    oppo_life = float(turn_row['oppo_life'])
    user_life = float(turn_row['user_life'])
    oppo_cards_in_hand = int(turn_row['oppo_cards_in_hand'])
    oppo_lands_in_play = int(turn_row['oppo_lands_in_play'])
    user_lands_in_play = int(turn_row['user_lands_in_play'])

    # Opponent's life and cards
    print(f"Turn {turn}")
    print(f"Opponent Life: {oppo_life}")
    print("Opponent Hand:")
    print(" ".join([card_box("???") for _ in range(oppo_cards_in_hand)]))  # Hidden cards
    print("Opponent Lands:")
    print(" ".join([card_box("Land") for _ in range(oppo_lands_in_play)]))  # Opponent's lands

    # Filter columns matching 'oppo_creature_<n>' and 'oppo_noncreature_<n>'
    oppo_creature_columns = [col for col in turn_row.index if 'oppo_creature' in col]
    oppo_noncreature_columns = [col for col in turn_row.index if 'oppo_noncreature' in col]

    # Extract non-null creature and non-creature names
    oppo_creatures = turn_row[oppo_creature_columns].dropna().values  # Filter out NaN
    oppo_noncreatures = turn_row[oppo_noncreature_columns].dropna().values

    # Format and display the opponent's board
    oppo_creature_print = " ".join([card_box(card) for card in oppo_creatures])
    oppo_noncreature_print = " ".join([card_box(card) for card in oppo_noncreatures])
    oppo_in_play_row = f"{oppo_creature_print}  ||  {oppo_noncreature_print}"
    print("Opponent Board:")
    print(oppo_in_play_row)

    print("\n" + "=" * 30 + "\n")  # Separator

    user_creature_columns = [col for col in turn_row.index if 'user_creature' in col]
    user_noncreature_columns = [col for col in turn_row.index if 'user_noncreature' in col]

    user_creatures = turn_row[user_creature_columns].dropna().values  # Filter out NaN
    user_noncreatures = turn_row[user_noncreature_columns].dropna().values

    user_creature_print = " ".join([card_box(card) for card in user_creatures])
    user_noncreature_print = " ".join([card_box(card) for card in user_noncreatures])
    user_in_play_row = f"{user_creature_print}  ||  {user_noncreature_print}"

    print(user_in_play_row)
    print("User Board:")

    user_lands = " ".join([card_box("Land") for _ in range(user_lands_in_play)])
    print(user_lands)
    print('User Lands:')

    user_hand_columns = [col for col in turn_row.index if 'user_hand' in col]
    user_hand = turn_row[user_hand_columns].dropna().values
    user_hand_print = " ".join([card_box(card) for card in user_hand])
    print(user_hand_print)
    print('User Hand:')
    print(f"User Life: {user_life}")

    # Filter columns matching 'user_creature_<n>' and 'user_noncreature_<n>'
    user_creature_columns = [col for col in turn_row.index if 'user_creature' in col]
    user_noncreature_columns = [col for col in turn_row.index if 'user_noncreature' in col]

    # Extract non-null creature and non-creature names for the user
    user_creatures = turn_row[user_creature_columns].dropna().values  # Filter out NaN
    user_noncreatures = turn_row[user_noncreature_columns].dropna().values

    # Format and display the user's board
    user_creature_print = " ".join([card_box(card) for card in user_creatures])
    user_noncreature_print = " ".join([card_box(card) for card in user_noncreatures])
