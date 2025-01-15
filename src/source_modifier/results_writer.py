import json
import csv


def save_results(results, output_file, output_format, first_write):
    """
    Save results to the specified output file and display them in the terminal.

    Args:
        results: List of results to save.
        output_file: Path to the output file.
        output_format: Format of the output file ('txt', 'csv', 'json').
        first_write: Whether to overwrite the file (True) or append (False).
    """
    write_mode = 'w' if first_write else 'a'  # Overwrite or append

    # Display results in the terminal
    print("\n--- Results ---\n")
    for result in results:
        if "search_text" in result:  # Text replacement results
            print(f"File: {result['file']}")
            print(f"  Line Number: {result['line_number']}")
            print(f"  Old Line: {result['old_line']}")
            print(f"  New Line: {result['new_line']}")
            print(f"  Search Text: {result['search_text']}")
            print(f"  Replace Text: {result['replace_text']}")
            print(f"  Occurrences: {result['occurrences']}\n")
        elif "json_path" in result:  # JSONPath replacement results
            print(f"File: {result['file']}")
            print(f"  JSON Path: {result['json_path']}")
            print(f"  Old Value: {result['old_value']}")
            print(f"  New Value: {result['new_value']}\n")
        elif "lines_inserted" in result: # Line insertion results
            print(f"File: {result['file']}")
            print(f"  {len(result['lines_inserted'])}) lines were {result['operation']} {result['insert_position']} at line number {result['line_number']}\n")

    # Save results to the specified output file
    if output_format == "txt":
        with open(output_file, write_mode, encoding="utf-8") as file:
            for result in results:
                file.write(f"File: {result['file']}\n")
                if "search_text" in result:
                    file.write(f"  Line Number: {result['line_number']}\n")
                    file.write(f"  Old Line: {result['old_line']}\n")
                    file.write(f"  New Line: {result['new_line']}\n")
                    file.write(f"  Search Text: {result['search_text']}\n")
                    file.write(f"  Replace Text: {result['replace_text']}\n")
                    file.write(f"  Occurrences: {result['occurrences']}\n\n")
                elif "json_path" in result:
                    file.write(f"  JSON Path: {result['json_path']}\n")
                    file.write(f"  Old Value: {result['old_value']}\n")
                    file.write(f"  New Value: {result['new_value']}\n\n")
                elif "lines_inserted" in result:
                    file.write(f"File: {result['file']}")
                    file.write(f"  {len(result['lines_inserted'])}) lines were {result['operation']} {result['insert_position']} at line number {result['line_number']}\n")

    elif output_format == "csv":
        with open(output_file, write_mode, newline='', encoding="utf-8") as file:
            if first_write:
                if "search_text" in results[0]:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=["file", "line_number", "old_line", "new_line", "search_text", "replace_text", "occurrences"],
                    )
                else:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=["file", "json_path", "old_value", "new_value"],
                    )
                writer.writeheader()
            else:
                if "search_text" in results[0]:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=["file", "line_number", "old_line", "new_line", "search_text", "replace_text", "occurrences"],
                    )
                elif "json_path" in results[0]:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=["file", "json_path", "old_value", "new_value"],
                    )
                elif "lines_inserted" in results[0]:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=["file", "lines_inserted", "operation", "insert_position", "line_number"],
                    )
            writer.writerows(results)

    elif output_format == "json":
        if first_write:
            with open(output_file, write_mode, encoding="utf-8") as file:
                json.dump(results, file, indent=4)
        else:
            with open(output_file, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
            existing_data.extend(results)
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4)

    print(f"Results saved to {output_file} in {output_format.upper()} format.")
