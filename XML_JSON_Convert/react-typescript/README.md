# XML ↔ JSON Converter (React + TypeScript)

Modern web application built with React, TypeScript, and Vite.

## Features

- Bidirectional conversion: XML ↔ JSON
- Fetch content from URL
- Upload/Download files
- Clear content with one click
- Type-safe TypeScript implementation

## Requirements

- Node.js 18+ (or Node.js 16+ with npm 7+)

> **Note:** React and all dependencies are installed locally via `npm install` - you don't need to install React globally. If you see TypeScript errors in your editor before running `npm install`, that's normal! The errors will disappear after installing dependencies.

---

## Installation & Usage

### Windows

```powershell
# Install dependencies
npm install

# Development mode
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

### Linux - Ubuntu / Debian

#### Install Node.js (if not installed)

```bash
# Option 1: Using NodeSource (recommended)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Option 2: Using snap
sudo snap install node --classic

# Option 3: Using nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
```

#### Verify installation

```bash
node --version
npm --version
```

#### Run the application

```bash
# Install dependencies
npm install

# Development mode (opens at http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

### Linux - Red Hat / Fedora / CentOS / RHEL

#### Install Node.js (if not installed)

```bash
# Option 1: Using NodeSource (RHEL/CentOS/Fedora)
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo dnf install -y nodejs

# For older systems using yum:
sudo yum install -y nodejs

# Option 2: Using dnf module (Fedora/RHEL 8+)
sudo dnf module install nodejs:20

# Option 3: Using nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
```

#### Verify installation

```bash
node --version
npm --version
```

#### Run the application

```bash
# Install dependencies
npm install

# Development mode (opens at http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Production Deployment

After building, the `dist/` folder contains static files that can be served by any web server:

```bash
# Build
npm run build

# Serve with any static server, e.g.:
npx serve dist
# or
python3 -m http.server 8080 -d dist
```

## Project Structure

```
react-typescript/
├── src/
│   ├── App.tsx         # Main React component
│   ├── converter.ts    # XML/JSON conversion logic
│   ├── styles.css      # Styling
│   └── main.tsx        # Entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html
```

## Dependencies

- React 18 - UI framework
- TypeScript - Type safety
- Vite - Build tool and dev server
