import os
from jsonpath_ng.ext import parse
from file_utils import load_file, save_file
from config_utils import load_config
from results_writer import save_results


def jsonpath_replace(content, rules):
    """
    Perform JSONPath-based replacement in JSON content.

    Args:
        content: The JSON object.
        rules: A list of rules with JSONPath expressions and replacements.

    Returns:
        content: The modified JSON object.
        results: A list of changes made.
    """
    results = []

    for rule in rules:
        if "jsonpath" not in rule or "replacement" not in rule:
            raise ValueError(f"Invalid rule format: {rule}. Each rule must contain 'jsonpath' and 'replacement' keys.")

        jsonpath_expr = parse(rule["jsonpath"])
        replacement = rule["replacement"]

        for match in jsonpath_expr.find(content):
            parent = match.context.value
            old_value = match.value
            new_value = replacement

            # Perform the replacement
            if isinstance(parent, dict):
                parent[match.path.fields[0]] = new_value
            elif isinstance(parent, list):
                parent[match.path.index] = new_value

            results.append({
                "json_path": str(match.full_path),
                "old_value": old_value,
                "new_value": new_value,
            })

    return content, results


def text_replace(content, rules):
    """
    Perform text replacement in plain text content.

    Args:
        content: The plain text content as a string.
        rules: A list of rules where each rule is a dictionary with keys:
            - `search`: Text to search for.
            - `replace`: Text to replace it with.

    Returns:
        updated_content: The modified text content as a list of lines.
        results: A list of changes made, including line numbers and old/new lines.
    """
    lines = content.splitlines()  # Split content into lines
    results = []

    for i, line in enumerate(lines):
        original_line = line
        for rule in rules:
            if "search" not in rule or "replace" not in rule:
                raise ValueError(f"Invalid rule format: {rule}. Each rule must contain 'search' and 'replace' keys.")

            search_text = rule["search"]
            replace_text = rule["replace"]

            if search_text in line:
                occurrences = line.count(search_text)
                line = line.replace(search_text, replace_text)
                results.append({
                    "line_number": i + 1,
                    "old_line": original_line,
                    "new_line": line,
                    "search_text": search_text,
                    "replace_text": replace_text,
                    "occurrences": occurrences,
                })

        lines[i] = line  # Update the line in place

    updated_content = "\n".join(lines)
    return updated_content, results


def process_file(file_path, config_file, output_file, output_format):
    """
    Process a single file as JSON or plain text based on its structure.
    """
    rules = load_config(config_file)
    content = load_file(file_path)

    if content is None:
        print(f"Error: Could not process the file '{file_path}'.")
        return

    # Determine if the file is JSON or plain text
    is_json = isinstance(content, (dict, list))

    if is_json:
        # Perform JSONPath-based replacement
        updated_content, results = jsonpath_replace(content, rules)
    else:
        # Perform plain text replacement
        updated_content, results = text_replace(content, rules)

    for result in results:
        result["file"] = file_path

    # Save the updated content back to the file
    save_file(file_path, updated_content)

    # Save and display results
    save_results(results, output_file, output_format)


def process_folder(folder, config_file, output_file, output_format):
    """
    Process all files in a folder.
    """
    rules = load_config(config_file)
    all_results = []

    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            content = load_file(file_path)

            if content is None:
                continue

            # Determine if the file is JSON or plain text
            is_json = isinstance(content, (dict, list))

            if is_json:
                # Perform JSONPath-based replacement
                updated_content, results = jsonpath_replace(content, rules)
            else:
                # Perform plain text replacement
                updated_content, results = text_replace(content, rules)

            for result in results:
                result["file"] = file_path

            all_results.extend(results)
            save_file(file_path, updated_content)

    save_results(all_results, output_file, output_format)
