# XML ↔ JSON Converter

A lightweight web application for bidirectional XML and JSON conversion.

## Features

- Bidirectional conversion: XML → JSON and JSON → XML
- Fetch content from URL (supports both XML and JSON endpoints)
- Upload files from local machine
- Download converted results
- Clear content with one click
- Cross-platform: Windows and Linux

## Requirements

- Python 3.7+

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Windows
```
run.bat
```
Or:
```
python app.py
```

### Linux
```bash
chmod +x run.sh
./run.sh
```
Or:
```bash
python app.py
```

Open http://localhost:5000 in your browser.

## How to Use

1. **Input data**: Paste content, upload a file, or fetch from URL
2. **Convert**: Click "XML → JSON" or "JSON → XML"
3. **Export**: Download the result or copy from the text area
4. **Clear**: Use the Clear button to reset a panel

## Dependencies

- Flask - Web framework
- xmltodict - XML/JSON conversion
- requests - HTTP requests
- waitress - Production WSGI server
