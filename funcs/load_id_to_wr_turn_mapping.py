import pandas as pd
def load_id_to_wr_turn_mapping(path_to_wr_by_turn_data = None):
    # wr_by_turn = pd.read_csv(r"C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\data\winrates_by_turn\dsk_winrates_by_turn.csv")
    if path_to_wr_by_turn_data:
        wr_by_turn = pd.read_csv(path_to_wr_by_turn_data)
    else:
        wr_by_turn = pd.read_csv(r"C:\Users\jwright\Documents\GitHub\sevLandsPublicData\data\winrates_by_turn\dsk_winrates_by_turn.csv")

    ## add this key to the data ahead of time so you don't need to do it in processing
    wr_by_turn['key'] = wr_by_turn['Card ID'].astype(int).astype(str) +"_" + wr_by_turn['Turn'].astype(str)
    output_dict = wr_by_turn[['key', 'Win Rate']].set_index('key')['Win Rate'].to_dict()

    
    return output_dict


if __name__ == '__main__':
    load_id_to_wr_turn_mapping()
