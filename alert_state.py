import pickle
import os

from pathlib import Path



def setup_alert():
    current_dir = os.getcwd()
    my_file = Path(current_dir + "/alert_state.p")
    if not my_file.exists():
        current_alert_state = 0
        pickle.dump( current_alert_state, open( my_file, "wb" ))
        print(f"alert state created")


def change_state(update_state):
    current_dir = os.getcwd()
    my_file = Path(current_dir + "/alert_state.p")
    if not my_file.exists():
        setup_alert()
    pickle.dump(update_state, open(my_file, "wb"))



def get_alert_state():
    current_dir = os.getcwd()
    my_file = Path(current_dir + "/alert_state.p")
    if not my_file.exists():
        setup_alert()
    current_alert_state = pickle.load(open( my_file, "rb" ))
    return current_alert_state
