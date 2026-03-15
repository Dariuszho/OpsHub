# XML ↔ JSON Converter

A collection of web applications for bidirectional XML and JSON conversion. Choose the version that best fits your needs.

## Projects

| Project                                 | Description                       | Requirements |
| --------------------------------------- | --------------------------------- | ------------ |
| [html-standalone](./html-standalone/)   | Single HTML file, no installation | Any browser  |
| [python-flask](./python-flask/)         | Server-based with URL proxy       | Python 3.7+  |
| [react-typescript](./react-typescript/) | Modern React/TypeScript app       | Node.js 18+  |

---

## Quick Comparison

### html-standalone
- ✅ Zero installation - just open in browser
- ✅ Works offline
- ✅ Single file, easy to share
- ⚠️ URL fetch limited by CORS

### python-flask
- ✅ Full URL fetch support (server proxy)
- ✅ Production-ready with Waitress
- ⚠️ Requires Python installed

### react-typescript
- ✅ Modern TypeScript codebase
- ✅ Component-based, easy to extend
- ✅ Fast development with hot reload
- ⚠️ Requires Node.js to build/run

---

## Features (All Versions)

- Bidirectional conversion: XML → JSON and JSON → XML
- Upload files from local machine
- Download converted results
- Clear content with one click
- Dark metallic UI theme

---

## Quick Start

### Simplest (No Installation)
```
Open html-standalone/index.html in your browser
```

### Python Version
```bash
cd python-flask
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

### React Version
```bash
cd react-typescript
npm install
npm run dev
# Open http://localhost:5173
```

---

## Platform Support

| Platform | html-standalone | python-flask | react-typescript |
| -------- | --------------- | ------------ | ---------------- |
| Windows  | ✅               | ✅            | ✅                |
| Linux    | ✅               | ✅            | ✅                |
| macOS    | ✅               | ✅            | ✅                |

See individual project READMEs for detailed installation instructions.
