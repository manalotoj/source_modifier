import os
from jsonpath_ng.ext import parse
from file_utils import load_file, save_file
from results_writer import save_results


def resolve_jsonpath_placeholders(transform_format, content, original_value):
    """
    Resolves placeholders in the transform_format using JSONPath expressions
    and the original value of the attribute.

    Args:
        transform_format: The format string with placeholders like `{jsonpath:<expression>}` or `{original}`.
        content: The full JSON content being processed.
        original_value: The original value of the attribute being modified.

    Returns:
        A string with all placeholders resolved and Python string operations applied.
    """
    import re

    # Regex to extract JSONPath placeholders
    placeholder_pattern = r"\{jsonpath:([^}]+)\}"

    # Context for string operations
    context = {"original": original_value}

    # Resolve JSONPath placeholders and add to the context
    def jsonpath_resolver(match):
        jsonpath_expr = match.group(1)
        jsonpath_compiled = parse(jsonpath_expr)
        results = [result.value for result in jsonpath_compiled.find(content)]
        resolved_value = results[0] if results else ""  # Use the first match or empty string
        placeholder = match.group(0)
        context[placeholder] = resolved_value  # Add resolved value to the context
        return placeholder  # Keep placeholder unchanged for later evaluation

    # Replace JSONPath placeholders with temporary placeholders in the string
    resolved_format = re.sub(placeholder_pattern, jsonpath_resolver, transform_format)

    # Evaluate the string with Python string operations
    try:
        # Use eval to apply string operations in a controlled environment
        resolved_format = eval(f'f"""{resolved_format}"""', {"__builtins__": None}, context)
    except Exception as e:
        raise ValueError(f"Error evaluating transform_format: {transform_format}. Error: {e}")

    return resolved_format


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
        if "jsonpath" not in rule:
            raise ValueError(f"Invalid rule format: {rule}. Each rule must contain 'jsonpath'.")

        jsonpath_expr = parse(rule["jsonpath"])
        replacement = rule.get("replacement")
        transform_format = rule.get("transform_format")

        for match in jsonpath_expr.find(content):
            parent = match.context.value
            old_value = match.value

            # Determine new value
            if transform_format:
                new_value = resolve_jsonpath_placeholders(transform_format, content, old_value)
            elif replacement is not None:
                new_value = replacement
            else:
                raise ValueError(f"Rule {rule} must specify either 'replacement' or 'transform_format'.")

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
        rules: A list of rules with 'search' and 'replace' keys.

    Returns:
        updated_content: The modified text content.
        results: A list of changes made.
    """
    lines = content.splitlines()
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


def process_file(file_path, config, output_file, output_format):
    """
    Process a single file as JSON or plain text based on its structure.

    Args:
        file_path: Path to the file to process.
        config: Parsed configuration containing the rules for processing.
        output_file: File to save the results.
        output_format: Format of the output (txt, csv, json).
    """
    all_results = []

    for rule in config:
        content = load_file(file_path)

        if content is None:
            print(f"Error: Could not process the file '{file_path}'.")
            continue

        # Determine if the file is JSON or plain text
        is_json = isinstance(content, (dict, list))

        if is_json and "jsonpath" in rule:
            updated_content, results = jsonpath_replace(content, [rule])
        elif not is_json and "search" in rule:
            updated_content, results = text_replace(content, [rule])
        else:
            print(f"Warning: Rule {rule} does not match the file type.")
            continue

        for result in results:
            result["file"] = file_path

        save_file(file_path, updated_content)
        all_results.extend(results)

    save_results(all_results, output_file, output_format)


def process_folder(folder, config, output_file, output_format):
    """
    Process all files in a folder.

    Args:
        folder: Path to the folder to process.
        config: Parsed configuration containing the rules for processing.
        output_file: File to save the results.
        output_format: Format of the output (txt, csv, json).
    """
    all_results = []

    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            for entry in config:
                content = load_file(file_path)

                if content is None:
                    continue

                is_json = isinstance(content, (dict, list))

                if is_json and "jsonpath" in entry:
                    updated_content, results = jsonpath_replace(content, [entry])
                elif not is_json and "search" in entry:
                    updated_content, results = text_replace(content, [entry])
                else:
                    continue

                for result in results:
                    result["file"] = file_path

                save_file(file_path, updated_content)
                all_results.extend(results)

    save_results(all_results, output_file, output_format)
