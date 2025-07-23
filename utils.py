import os
import json
from datetime import datetime

def load_settings(settings_file):
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_settings(settings_file, settings):
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")