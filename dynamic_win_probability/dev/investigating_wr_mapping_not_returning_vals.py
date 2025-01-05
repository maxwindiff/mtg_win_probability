import os
import pandas as pd
import sys
os.chdir(r"C:\Users\jwright\Documents\GitHub\sevLandsPublicData\dynamic_win_probability")
current_dir = os.path.dirname(os.path.abspath(__file__))
funcs_dir = os.path.join(current_dir, 'funcs')
if funcs_dir not in sys.path:
    sys.path.append(funcs_dir)

from funcs.load_id_to_wr_mapping import load_id_to_wr_mapping


print(load_id_to_wr_mapping())