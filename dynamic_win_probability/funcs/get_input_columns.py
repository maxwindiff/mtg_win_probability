def get_input_columns(num_turns = 20):
    static_columns = ['draft_id', 'num_turns', 'on_play', 'won']
    dynamic_columns = []
    
    for turn in range(1, num_turns + 1):
        for player in ['user', 'oppo']:
            dynamic_columns.extend([
                f'{player}_turn_{turn}_eot_{player}_cards_in_hand',
                f'{player}_turn_{turn}_eot_{player}_lands_in_play',
                f'{player}_turn_{turn}_eot_{player}_creatures_in_play',
                f'{player}_turn_{turn}_eot_{player}_non_creatures_in_play',
                f'{player}_turn_{turn}_eot_{player}_life',
            ])
    
    return static_columns + dynamic_columns