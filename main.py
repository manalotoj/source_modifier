import argparse
import os
from processor import process_file, process_folder

def main():
    parser = argparse.ArgumentParser(description="Perform text replacements in files.")
    parser.add_argument("path", help="Path to a file or folder containing files to process.")
    parser.add_argument("config", help="Configuration file specifying search and replace rules.")
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

    # Check if the input path is a file or a folder
    if os.path.isfile(args.path):
        process_file(args.path, args.config, args.output, args.format)
    elif os.path.isdir(args.path):
        process_folder(args.path, args.config, args.output, args.format)
    else:
        print(f"Error: The specified path '{args.path}' is neither a file nor a folder.")

if __name__ == "__main__":
    main()
