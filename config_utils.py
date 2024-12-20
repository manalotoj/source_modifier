import json

def load_config(config_file):
    """Load the search and replace configuration."""
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config file {config_file}: {e}")
        return []
