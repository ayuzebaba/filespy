# filespy

A command line tool for analyzing files and folders built with Python.

## Installation
```bash
pip install -e .
```

## Usage

### Analyze a single file
```bash
filespy analyze sample.txt
```

### Scan a folder
```bash
filespy scan .
```

### Scan a folder filtering by extension
```bash
filespy scan . --extension .txt
```

## Example Output
```
File:       sample.txt
Lines:      3
Words:      28
Size:       0.14 KB
Extension:  .txt
```

## Logging

filespy logs everything to `filespy.log` in your project folder.
The terminal shows INFO and above.
The log file records everything including DEBUG.

## Project Structure
```
filespy/
├── src/
│   └── filespy/
│       ├── __init__.py
│       ├── analyzer.py   ← core functions
│       ├── cli.py        ← terminal commands
│       └── logger.py     ← logging setup
├── tests/
│   └── test_analyzer.py
└── pyproject.toml
```

## Requirements

- Python 3.8+
- click
- fastapi
- uvicorn
- pytest