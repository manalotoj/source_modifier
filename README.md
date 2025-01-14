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

### **From PyPI (Coming Soon)**
```bash
pip install source-modifier
```

### **From Source**
1. Clone the repository:
   ```bash
   git clone https://github.com/manalotoj/source_modifier.git
   cd source_modifier
   ```

2. Build and install:
   ```bash
   python -m build
   pip install dist/source_modifier-0.1.0-py3-none-any.whl
   ```

---

## **Usage**

### **Command-Line Interface**
Run the tool from the command line:
```bash
source_modifier --config <config.json> --output <output.txt> [--plan | --apply]
```

#### **Options**
- `--config`: Path to the configuration file defining search-and-replace rules.
- `--output`: Path to save the results.
- `--plan`: Preview changes without applying them.
- `--apply`: Apply changes directly to the files.

#### **Example**
```bash
source_modifier --config config.json --output results.json --plan
```

### **As a Python Library**
Import the package in your Python scripts:
```python
from source_modifier.main import main

main()
```

---

## **Configuration File**
The configuration file is a JSON file containing a list of rules. Each rule defines:
- `path`: File or directory to process.
- `search`: Text to search for (text files).
- `replace`: Replacement text (text files).
- `jsonpath`: JSONPath query for locating elements (JSON files).
- `replacement`: Value to replace the matched JSONPath.

### **Example Configuration**
```json
[
    {
        "path": "data/input.json",
        "jsonpath": "$.items[*].name",
        "replacement": "Updated Name"
    },
    {
        "path": "data/example.txt",
        "search": "foo",
        "replace": "bar"
    }
]
```

---

## **Development**

### **Requirements**
Install dependencies for development:
```bash
pip install -r requirements-dev.txt
```

### **Testing**
Run tests using `pytest`:
```bash
pytest tests/
```

### **Build the Project**
```bash
python -m build
```

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## **Contributing**
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

---

## **Links**
- **Homepage**: [GitHub Repository](https://github.com/manalotoj/source_modifier)
- **Issues**: [Report a Bug](https://github.com/manalotoj/source_modifier/issues)

