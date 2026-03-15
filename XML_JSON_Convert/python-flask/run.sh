#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt
echo
echo "Starting XML to JSON Converter..."
echo "Open http://localhost:5000 in your browser"
python app.py
