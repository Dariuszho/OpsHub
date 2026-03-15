"""
XML ↔ JSON Converter Web Application
Works on Windows and Linux
"""
from flask import Flask, request, render_template, jsonify
import xmltodict
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_content():
    try:
        url = request.form.get('url', '').strip()
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        return jsonify({'content': response.text})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch URL: {str(e)}'}), 400

@app.route('/convert', methods=['POST'])
def convert():
    try:
        direction = request.form.get('direction', '')
        content = request.form.get('content', '').strip()
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        if direction == 'toJson':
            parsed = xmltodict.parse(content)
            result = json.dumps(parsed, indent=2)
        elif direction == 'toXml':
            parsed = json.loads(content)
            result = xmltodict.unparse(parsed, pretty=True)
        else:
            return jsonify({'error': 'Invalid direction'}), 400
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    from waitress import serve
    print("Starting server at http://localhost:5000")
    serve(app, host='0.0.0.0', port=5000)
