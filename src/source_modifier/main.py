import argparse
import os
from source_modifier.processor import process_file, process_folder
from source_modifier.file_utils import load_file
from source_modifier.results_writer import save_results


def infer_output_format(output_file):
    """
    Infer the output format from the file extension.

    Args:
        output_file: Path to the output file.

    Returns:
        The inferred output format ('txt', 'csv', or 'json').
    """
    print("output_file:", output_file)
    ext = os.path.splitext(output_file)[1].lower()
    if ext == ".txt":
        return "txt"
    elif ext == ".csv":
        return "csv"
    elif ext == ".json":
        return "json"
    else:
        raise ValueError(f"Unsupported file extension: {ext}. Supported extensions are .txt, .csv, .json.")


def main():
    parser = argparse.ArgumentParser(description="Perform search and replace on JSON or text files.")
    parser.add_argument("config", help="Path to the configuration file.")
    parser.add_argument("-o", "--output", help="Path to the output results file.", required=True)
    parser.add_argument("-p", "--plan", action="store_true", help="Plan the changes without applying them.")
    parser.add_argument("-a", "--apply", action="store_true", help="Apply the changes to the target files.")
    args = parser.parse_args()

    if args.plan and args.apply:
        raise ValueError("Both --plan and --apply cannot be specified together. Choose one.")

    if not args.plan and not args.apply:
        args.plan = True  # Default behavior is plan mode

    config = load_file(args.config)
    if not isinstance(config, list):
        raise ValueError("Configuration file must contain a list of rules.")

    output_file = args.output
    output_format = infer_output_format(output_file)
    first_write = True  # Flag to control whether to overwrite or append

    for entry in config:
        path = entry.get("path")
        if not path:
            print("Error: Each configuration entry must include a 'path'.")
            continue

        if os.path.isfile(path):
            print(f"Processing file: {path}")
            results = process_file(path, [entry], collect_results=True, plan=args.plan)
        elif os.path.isdir(path):
            print(f"Processing folder: {path}")
            results = process_folder(path, [entry], collect_results=True, plan=args.plan)
        else:
            print(f"Error: Path '{path}' is not valid.")
            continue

        # Save results to output file
        save_results(results, output_file, output_format, first_write)

        # Set flag to append for subsequent writes
        first_write = False


if __name__ == "__main__":
    main()
