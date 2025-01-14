# **Source Modifier**

A Python-based tool for modifying source code with advanced search-and-replace functionality. Designed for ease of use, scalability, and flexibility.

---

## **Features**
- **Search and Replace**: Perform targeted modifications in JSON and text files.
- **JSONPath Support**: Use JSONPath for precise queries and transformations.
- **Batch Processing**: Process individual files or entire directories.
- **Plan or Apply**: Preview changes with "plan mode" before applying them.

---

## **Installation**

### **From GitHub Releases**
1. Download the latest release from the [GitHub Releases page](https://github.com/manalotoj/source_modifier/releases).

2. Install the downloaded wheel file:
   ```bash
   pip install source_modifier-<version>-py3-none-any.whl
   ```

---

## **Usage**

### **Command-Line Interface**
Run the tool from the command line:
```bash
source_modifier <config_file> -o <output_file> [-p | -a]
```

#### **Options**
- `<config_file>`: Path to the configuration file defining search-and-replace rules.
- `-o/--output`: Path to save the results.
- `-p/--plan`: Preview changes without applying them.
- `-a/--apply`: Apply changes directly to the files.

#### **Example**
```bash
source_modifier config.json -o results.json -p
```

---

## **Configuration File**
The configuration file is a JSON file containing a list of rules. Each rule defines:
- **Plain Text Search and Replace**: Use `search`, `replace`, and `path` properties.
- **JSON Modification**: Use `path`, `jsonpath`, and either `replacement` or `transform` properties. If both `replacement` and `transform` are provided, `transform` takes precedence.

### **Example Configuration**
```json
[
    {
        "path": "./sample_target/Deploy-VM-DataDiskSpace-Alert.json",
        "jsonpath": "$..query",
        "replacement": "[format('let policyThresholdString = \"{0}\"; InsightsMetrics | where _ResourceId has \"Microsoft.Compute/virtualMachines\" | where Origin == \"vm.azm.ms\" | where Namespace == \"LogicalDisk\" and Name == \"FreeSpacePercentage\" | extend Disk=tostring(todynamic(Tags)[\"vm.azm.ms/mountId\"]) | where Disk !in (\"C:\\\",\"/\") | summarize AggregatedValue = avg(Val) by bin(TimeGenerated, 15m), Computer, _ResourceId, Disk | extend appliedThresholdString = policyThresholdString | extend appliedThreshold = toint(appliedThresholdString) | where AggregatedValue < appliedThreshold | project TimeGenerated, Computer, _ResourceId, Disk, AggregatedValue', parameters('threshold'))]"
    },
    {
        "path": "./sample_target/Deploy-VM-DataDiskSpace-Alert.json",
        "jsonpath": "$..deployment..properties.description",
        "transform": "{original} ---AND--- {original}"
    },
    { 
        "search": "northeurope", 
        "replace": "usgovarizona", 
        "path": "./sample_target" 
    }
]
```

#### **Explanation of the Configuration**

1. **First Entry:**
   - This rule replaces the entire value of a JSON property located using the JSONPath expression `$..query`.
   - The `replacement` field specifies the new value to be assigned, which includes a complex query string.
   - **JSONPath Usage:** JSONPath allows precise targeting of the `query` property across the JSON file.

2. **Second Entry:**
   - This rule uses the `transform` field to modify the `description` attribute found via the JSONPath expression `$..deployment..properties.description`.
   - The `transform` field supports Python string interpolation and operations. Here, `{original}` is used to reference the current value of the JSON property, enabling dynamic modifications like appending or altering content.
   - **Dynamic Transformation:**
     - The `transform` field allows referencing other JSON attributes or values dynamically within the same JSON file.
     - Python expressions can be used to construct or modify the new value based on the current context of the JSON attribute.

3. **Third Entry:**
   - This is a straightforward text search-and-replace rule.
   - It searches for the string `northeurope` within text files or directories under `./sample_target` and replaces it with `usgovarizona`.
   - **Plain Text Replacement:** No JSON-specific logic is applied here, making it suitable for modifying plain text files.

