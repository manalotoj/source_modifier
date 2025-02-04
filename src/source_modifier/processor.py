import os
import json
from jsonpath_ng.ext import parse
from source_modifier.file_utils import load_file, save_file

def insert_lines_by_line_number(content, rules):
    """
    Insert lines into the content based on line numbers.

    Parameters:
        content (str): The file content as a string.
        rules (list of dict): List of insertion rules. Each rule must contain:
            - 'line_number': The line number for insertion (1-based indexing).
            - 'insert_position': Either 'before' or 'after'.
            - 'lines': List of lines to insert.

    Returns:
        str: The updated content.
        list: The results of the operation.
    """
    lines = content.splitlines()
    results = []

    for rule in rules:
        operation = rule.get("operation")
        line_number = rule.get("line_number")
        insert_position = rule.get("insert_position", "after")
        new_lines = rule.get("lines", [])

        if operation != "insert":
            raise ValueError(f"Unsupported operation: {operation}.")
        if not isinstance(line_number, int) or line_number < 1 or line_number > len(lines) + 1:
            raise ValueError(f"Invalid line number: {line_number}.")
        if insert_position not in ["before", "after"]:
            raise ValueError(f"Invalid insert_position: {insert_position}. Must be 'before' or 'after'.")

        # Adjust for 0-based indexing
        line_index = line_number - 1

        # Determine where to insert
        insert_index = line_index if insert_position == "before" else line_index + 1

        # Insert new lines
        for new_line in reversed(new_lines):  # Reverse to maintain order when inserting
            lines.insert(insert_index, new_line)

        results.append({
            "operation": operation,
            "line_number": line_number,
            "insert_position": insert_position,
            "lines_inserted": new_lines,
        })

    return "\n".join(lines), results

def resolve_jsonpath_placeholders(transform, content, original_value):
    import re

    placeholder_pattern = r"\{jsonpath:([^}]+)\}"
    context = {"original": original_value}

    def jsonpath_resolver(match):
        jsonpath_expr = match.group(1)
        jsonpath_compiled = parse(jsonpath_expr)
        results = [result.value for result in jsonpath_compiled.find(content)]
        return results[0] if results else ""

    resolved_transform = re.sub(placeholder_pattern, jsonpath_resolver, transform)

    try:
        resolved_transform = eval(f'f"""{resolved_transform}"""', {"__builtins__": None}, context)
    except Exception as e:
        raise ValueError(f"Error evaluating transform: {transform}. Error: {e}")

    return resolved_transform


def jsonpath_replace(content, rules):
    results = []

    for rule in rules:
        if "jsonpath" not in rule:
            raise ValueError(f"Invalid rule format: {rule}. Each rule must contain 'jsonpath'.")

        jsonpath_expr = parse(rule["jsonpath"])
        replacement = rule.get("replacement")
        transform = rule.get("transform")

        for match in jsonpath_expr.find(content):
            parent = match.context.value
            old_value = match.value

            if transform:
                new_value = resolve_jsonpath_placeholders(transform, content, old_value)
            elif replacement is not None:
                new_value = replacement
            else:
                raise ValueError(f"Rule {rule} must specify either 'replacement' or 'transform'.")

            if old_value != new_value:  # Only update if there's a change
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
    lines = content.splitlines()
    results = []

    for i, line in enumerate(lines):
        original_line = line
        for rule in rules:
            if "search" not in rule or "replacement" not in rule:
                raise ValueError(f"Invalid rule format: {rule}. Each rule must contain 'search' and 'replace' keys.")

            search_text = rule["search"]
            replace_text = rule["replacement"]

            if search_text in line:
                occurrences = line.count(search_text)
                updated_line = line.replace(search_text, replace_text)
                lines[i] = updated_line  # Update the modified line
                results.append({
                    "line_number": i + 1,
                    "old_line": original_line,
                    "new_line": updated_line,
                    "search_text": search_text,
                    "replace_text": replace_text,
                    "occurrences": occurrences,
                })

    updated_content = "\n".join(lines)
    return updated_content, results


def process_file(file_path, config, collect_results=False, plan=True):
    all_results = []
    content = load_file(file_path)

    if content is None:
        print(f"Error: Could not process the file '{file_path}'.")
        return []

    is_json = isinstance(content, (dict, list))
    updated_content = content

    for rule in config:
        results = []

        # Apply line modification based on line number
        if "line_number" in rule:
            string_content = json.dumps(updated_content, indent=4) if is_json else updated_content
            string_content, modify_results = insert_lines_by_line_number(string_content, [rule])
            results.extend(modify_results)

            updated_content = json.loads(string_content) if is_json else string_content

        # Apply JSONPath replacement if the rule specifies jsonpath
        if "jsonpath" in rule and is_json:
            updated_content, json_results = jsonpath_replace(updated_content, [rule])
            results.extend(json_results)

        # Apply text replacement if the rule specifies search/replace
        elif "search" in rule and "replacement" in rule:
            string_content = json.dumps(updated_content, indent=4) if is_json else updated_content
            string_content, text_results = text_replace(string_content, [rule])
            results.extend(text_results)

            updated_content = json.loads(string_content) if is_json else string_content

        for result in results:
            result["file"] = file_path

        all_results.extend(results)

    # Save the modified content to the file only if not in plan mode
    if not plan:
        save_file(file_path, updated_content)

    return all_results


def process_folder(folder, config, collect_results=False, plan=True):
    all_results = []

    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_results = process_file(file_path, config, collect_results=True, plan=plan)
            all_results.extend(file_results)

    return all_results
