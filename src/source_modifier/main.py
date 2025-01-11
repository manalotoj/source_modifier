import argparse
import os
from processor import process_file, process_folder
from file_utils import load_file


def main():
    parser = argparse.ArgumentParser(description="Perform search and replace on JSON or text files.")
    parser.add_argument("config", help="Path to the configuration file.")
    parser.add_argument("-o", "--output", help="Path to the output results file.", required=True)
    parser.add_argument("-f", "--format", help="Output format: txt, csv, or json.", default="txt")
    args = parser.parse_args()

    config = load_file(args.config)
    if not isinstance(config, list):
        raise ValueError("Configuration file must contain a list of rules.")

    output_file = args.output
    output_format = args.format
    first_write = True  # Flag to control whether to overwrite or append

    for entry in config:
        path = entry.get("path")
        if not path:
            print("Error: Each configuration entry must include a 'path'.")
            continue

        if os.path.isfile(path):
            print(f"Processing file: {path}")
            results = process_file(path, [entry], collect_results=True)
        elif os.path.isdir(path):
            print(f"Processing folder: {path}")
            results = process_folder(path, [entry], collect_results=True)
        else:
            print(f"Error: Path '{path}' is not valid.")
            continue

        # Save results to output file
        from results_writer import save_results
        save_results(results, output_file, output_format, first_write)

        # Set flag to append for subsequent writes
        first_write = False


if __name__ == "__main__":
    main()
