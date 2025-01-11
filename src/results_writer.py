import json
import csv

def save_results(results, output_file, output_format):
    """Save results to the specified output file and display them in the terminal."""
    
    # Display results in the terminal
    print("\n--- Results ---\n")
    for result in results:
        print(f"File: {result['file']}")
        if "line_number" in result:  # For plain text replacements
            print(f"  Line Number: {result['line_number']}")
            print(f"  Old Line: {result['old_line']}")
            print(f"  New Line: {result['new_line']}")
        elif "json_path" in result:  # For JSONPath-based replacements
            print(f"  JSON Path: {result['json_path']}")
            print(f"  Old Value: {result['old_value']}")
            print(f"  New Value: {result['new_value']}")
        print()

    # Save results to the specified output file
    if output_format == "txt":
        with open(output_file, 'w') as file:
            for result in results:
                file.write(f"File: {result['file']}\n")
                if "line_number" in result:
                    file.write(f"  Line Number: {result['line_number']}\n")
                    file.write(f"  Old Line: {result['old_line']}\n")
                    file.write(f"  New Line: {result['new_line']}\n")
                elif "json_path" in result:
                    file.write(f"  JSON Path: {result['json_path']}\n")
                    file.write(f"  Old Value: {result['old_value']}\n")
                    file.write(f"  New Value: {result['new_value']}\n")
                file.write("\n")

    elif output_format == "csv":
        with open(output_file, 'w', newline='') as file:
            if "line_number" in results[0]:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["file", "line_number", "old_line", "new_line", "search_text", "replace_text", "occurrences"]
                )
            else:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["file", "json_path", "old_value", "new_value"]
                )
            writer.writeheader()
            writer.writerows(results)

    elif output_format == "json":
        with open(output_file, 'w') as file:
            json.dump(results, file, indent=4)

    print(f"\nResults saved to {output_file} in {output_format.upper()} format.")
