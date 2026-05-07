# PDF Merger

A lightweight, browser-based tool for merging multiple PDF files into one — no server, no installation, no data upload.

Created by **Dariusz**.

---

## Files

| File                     | Description     |
| ------------------------ | --------------- |
| `PDF_Merger_Hebrew.html` | Hebrew varian   |
| `PDF_Merger_Eng.html`    | English variant |

---

## How to use

1. Open `PDF_Merger.html` in any modern browser.
2. Click the drop zone or drag PDF files onto it.
3. Reorder files using the ▲ / ▼ buttons or by dragging rows.
4. Remove unwanted files with the ✕ button.
5. Click **Merge & Download** — the merged PDF downloads automatically.

The **Merge & Download** button is disabled until at least 2 files are selected.

---

## Features

- Drag-and-drop file input
- Manual reordering (drag rows or arrow buttons)
- Remove individual files from the list
- Client-side only — files never leave your machine
- Merged file is named `merged_<timestamp>.pdf`

---

## Requirements

- A modern browser (Chrome, Edge, Firefox, Safari)
- No internet connection required after the page loads (pdf-lib is loaded from CDN on first open)

---

## Dependencies

- [pdf-lib](https://pdf-lib.js.org/) — loaded via CDN (`unpkg.com`)
