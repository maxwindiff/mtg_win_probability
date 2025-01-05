import joblib
import os
class PhaseBasedModel:
    def __init__(self):
        print('current working directory: ', os.getcwd())
        # Load pre-trained models
        self.early_model = joblib.load('../models/win_probability/phase_models/xgboost_early_game.pkl')
        self.mid_model = joblib.load('../models/win_probability/phase_models/xgboost_mid_game.pkl')
        self.late_model = joblib.load('../models/win_probability/phase_models/random_forest_late_game.pkl')
        
    def predict(self, data):
        if 'game_id' in data.columns:
            data = data.drop(columns='game_id')
        if 'unique_id' in data.columns:
            data = data.drop(columns='unique_id')
        # Determine the phase based on the turn number
        turn = data['turn'].iloc[0]  # Assuming batch predictions are per phase
        if 1 <= turn <= 5:
            model = self.early_model
        elif 6 <= turn <= 10:
            model = self.mid_model
        else:
            model = self.late_model
        
        # Remove phase-specific columns
        X = data.drop(columns=['turn', 'won'], errors='ignore')
        return model.predict(X)
