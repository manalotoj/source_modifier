import json

def load_file(file_path):
    """
    Load a file as either JSON or plain text based on its content.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        try:
            return json.loads(content)  # Attempt to parse as JSON
        except json.JSONDecodeError:
            return content  # Fallback to plain text
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None

def save_file(file_path, content):
    """
    Save a file as either JSON or plain text based on its content.
    """
    try:
        with open(file_path, 'w') as file:
            if isinstance(content, (dict, list)):
                json.dump(content, file, indent=4)
            else:
                file.write(content)
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")
