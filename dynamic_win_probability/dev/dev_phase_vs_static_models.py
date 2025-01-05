import sys
import os 
import pandas as pd
import random

# Set working directory
os.chdir(r'C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\dynamic_win_probability')
print(os.listdir())
# Add folder funcs to path
sys.path.append(r'C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\dynamic_win_probability\funcs')
sys.path.append(r'C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\dynamic_win_probability\Classes')
from PhaseBasedModel import PhaseBasedModel
from transform_replay_data import transform_replay_data
import pickle

# Load static model
with open(r'C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\models\win_probability\xgb_win_prob_model.pkl', 'rb') as file:
    static_model = pickle.load(file)



# Load data
# Define the number of rows you want to sample


# Get the total number of rows in the file (including header)
file_path = r"C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\data\replay_data\replay_data_public.DSK.PremierDraft.csv"
data = pd.read_csv(file_path, nrows=10000)
# Read only the sampled rows)
dynamic_data = transform_replay_data(data, dynamic_winrate=True)
static_data = transform_replay_data(data, dynamic_winrate=False)
print('data loaded: loading PhaseBasedModel')
# Initialize PhaseBasedModel
p = PhaseBasedModel()

print('PhaseBasedModel loaded: predicting')
# Make predictions
dynamic_predictions = p.predict(dynamic_data)
static_predictions = static_model.predict(static_data.drop(columns=['game_id','unique_id', 'won'], errors='ignore'))
# Compare predictions to reality
dynamic_correct = dynamic_data['won'] 
static_correct = static_data['won']
dynamic_accuracy = (dynamic_predictions == dynamic_correct.values).mean()
static_accuracy = (static_predictions == static_correct.values).mean()
print(f"Dynamic model accuracy: {dynamic_accuracy}")
print(f"Static model accuracy: {static_accuracy}")