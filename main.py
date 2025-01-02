import argparse
import os
from processor import process_file, process_folder
from config_utils import load_config

def main():
    parser = argparse.ArgumentParser(description="Perform text or JSONPath replacements in files or folders.")
    parser.add_argument("config", help="Path to the configuration file specifying search and replace rules.")
    parser.add_argument(
        "-o", "--output", default="results.txt", help="Output file to save the results (default: results.txt)."
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["txt", "csv", "json"],
        default="txt",
        help="Output format for the results: txt, csv, or json (default: txt).",
    )
    args = parser.parse_args()

    # Load the configuration file
    try:
        config = load_config(args.config)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Process each entry in the configuration
    for entry in config:
        path = entry["path"]
        if os.path.isfile(path):
            print(f"Processing file: {path}")
            process_file(path, [entry], args.output, args.format)
        elif os.path.isdir(path):
            print(f"Processing folder: {path}")
            process_folder(path, [entry], args.output, args.format)
        else:
            print(f"Error: Path '{path}' is neither a valid file nor a folder.")

if __name__ == "__main__":
    main()
