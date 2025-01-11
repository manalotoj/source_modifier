import json
import os

def load_config(config_file):
    """
    Load and validate the configuration file.
    Ensures each entry contains a valid 'path' key pointing to a file or folder.
    """
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)

        # Validate each entry
        if not isinstance(config, list):
            raise ValueError("The configuration file must contain a list of entries.")
        for entry in config:
            if "path" not in entry:
                raise ValueError(f"Config entry {entry} is missing the 'path' key.")
            if not os.path.exists(entry["path"]):
                raise ValueError(f"Path '{entry['path']}' does not exist.")
            if "jsonpath" not in entry and "search" not in entry:
                raise ValueError(f"Config entry {entry} must have either 'jsonpath' or 'search'.")
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Configuration file '{config_file}' is not valid JSON: {e}")
    except Exception as e:
        raise ValueError(f"Error loading config file '{config_file}': {e}")
