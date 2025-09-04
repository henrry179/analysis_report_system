#!/bin/bash

# QWCoder Project Templates Generator
# Creates project templates for various frameworks and languages

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create Node.js project
create_nodejs_project() {
    local project_name="$1"
    local template="$2"

    log_info "Creating Node.js project: $project_name"

    mkdir -p "$project_name"
    cd "$project_name"

    # Initialize package.json
    cat > package.json << EOF
{
  "name": "$project_name",
  "version": "1.0.0",
  "description": "A Node.js project created with QWCoder",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "devDependencies": {
    "nodemon": "^2.0.20",
    "jest": "^29.3.1",
    "eslint": "^8.28.0",
    "prettier": "^2.8.0"
  }
}
EOF

    # Create basic files
    cat > index.js << EOF
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Hello from $project_name!' });
});

app.listen(port, () => {
  console.log(\`Server running on port \${port}\`);
});
EOF

    # Create README
    cat > README.md << EOF
# $project_name

A Node.js project created with QWCoder.

## Getting Started

1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Start development server:
   \`\`\`bash
   npm run dev
   \`\`\`

3. Run tests:
   \`\`\`bash
   npm test
   \`\`\`

## Available Scripts

- \`npm start\` - Start production server
- \`npm run dev\` - Start development server with nodemon
- \`npm test\` - Run tests
- \`npm run lint\` - Lint code
- \`npm run format\` - Format code

## Project Structure

\`\`\`
$project_name/
├── index.js          # Main application file
├── package.json      # Dependencies and scripts
├── README.md         # This file
└── node_modules/     # Dependencies (created after npm install)
\`\`\`
EOF

    # Create .gitignore
    cat > .gitignore << EOF
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage
.grunt

# Bower dependency directory
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons
build/Release

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF

    # Create ESLint config
    cat > .eslintrc.js << EOF
module.exports = {
  env: {
    node: true,
    es2022: true,
  },
  extends: ['eslint:recommended'],
  parserOptions: {
    ecmaVersion: 'latest',
  },
  rules: {
    'no-unused-vars': 'warn',
    'no-console': 'off',
  },
};
EOF

    # Create Prettier config
    cat > .prettierrc << EOF
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
EOF

    log_success "Node.js project '$project_name' created successfully!"
    log_info "Next steps:"
    log_info "  cd $project_name"
    log_info "  npm install"
    log_info "  npm run dev"
}

# Create Python project
create_python_project() {
    local project_name="$1"
    local template="$2"

    log_info "Creating Python project: $project_name"

    mkdir -p "$project_name"
    cd "$project_name"

    # Create virtual environment
    python3 -m venv venv

    # Create requirements.txt
    cat > requirements.txt << EOF
# Web Framework
flask==2.3.2
fastapi==0.88.0
uvicorn==0.20.0

# Data Science
pandas==1.5.2
numpy==1.24.1
matplotlib==3.6.2
scikit-learn==1.2.0

# Development
pytest==7.2.0
black==22.12.0
flake8==6.0.0
mypy==0.991

# Utilities
requests==2.28.1
python-dotenv==0.21.0
click==8.1.3
EOF

    # Create main.py
    cat > main.py << EOF
#!/usr/bin/env python3
"""
$project_name - A Python project created with QWCoder
"""

def main():
    print("Hello from $project_name!")
    print("Edit main.py to start building your application.")

if __name__ == "__main__":
    main()
EOF

    # Create test file
    mkdir -p tests
    cat > tests/__init__.py << EOF
# Test package
EOF

    cat > tests/test_main.py << EOF
import pytest
from main import main

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from $project_name!" in captured.out
EOF

    # Create README
    cat > README.md << EOF
# $project_name

A Python project created with QWCoder.

## Getting Started

1. Activate virtual environment:
   \`\`\`bash
   source venv/bin/activate  # Linux/Mac
   # or
   venv\\Scripts\\activate     # Windows
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Run the application:
   \`\`\`bash
   python main.py
   \`\`\`

4. Run tests:
   \`\`\`bash
   pytest
   \`\`\`

## Available Commands

- \`python main.py\` - Run main application
- \`pytest\` - Run tests
- \`black .\` - Format code
- \`flake8 .\` - Lint code
- \`mypy .\` - Type check

## Project Structure

\`\`\`
$project_name/
├── main.py           # Main application file
├── requirements.txt  # Python dependencies
├── tests/            # Test files
│   ├── __init__.py
│   └── test_main.py
├── venv/             # Virtual environment
└── README.md         # This file
\`\`\`
EOF

    # Create .gitignore
    cat > .gitignore << EOF
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF

    # Create Python configuration files
    cat > .flake8 << EOF
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,build,dist,venv
EOF

    cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 22.12.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
EOF

    log_success "Python project '$project_name' created successfully!"
    log_info "Next steps:"
    log_info "  cd $project_name"
    log_info "  source venv/bin/activate"
    log_info "  pip install -r requirements.txt"
    log_info "  python main.py"
}

# Create React project
create_react_project() {
    local project_name="$1"
    local template="$2"

    log_info "Creating React project: $project_name"

    # Check if npx is available
    if ! command -v npx >/dev/null 2>&1; then
        log_error "npx not found. Please install Node.js first."
        return 1
    fi

    # Create React app
    npx create-react-app "$project_name" --yes

    cd "$project_name"

    # Create additional directories
    mkdir -p src/components src/hooks src/utils src/styles

    # Create a simple component
    cat > src/components/Welcome.js << EOF
import React from 'react';

function Welcome() {
  return (
    <div className="welcome">
      <h1>Welcome to $project_name!</h1>
      <p>This React app was created with QWCoder.</p>
    </div>
  );
}

export default Welcome;
EOF

    # Update App.js
    cat > src/App.js << EOF
import React from 'react';
import Welcome from './components/Welcome';
import './App.css';

function App() {
  return (
    <div className="App">
      <Welcome />
    </div>
  );
}

export default App;
EOF

    # Create custom styles
    cat > src/styles/global.css << EOF
/* Global styles for $project_name */

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.welcome {
  text-align: center;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.welcome h1 {
  color: #282c34;
  margin-bottom: 1rem;
}

.welcome p {
  color: #666;
  font-size: 1.2rem;
  line-height: 1.6;
}
EOF

    # Update App.css to import global styles
    echo "@import './styles/global.css';" > src/App.css

    log_success "React project '$project_name' created successfully!"
    log_info "Next steps:"
    log_info "  cd $project_name"
    log_info "  npm start"
}

# Create Go project
create_go_project() {
    local project_name="$1"
    local template="$2"

    log_info "Creating Go project: $project_name"

    # Check if go is available
    if ! command -v go >/dev/null 2>&1; then
        log_error "Go not found. Please install Go first."
        return 1
    fi

    mkdir -p "$project_name"
    cd "$project_name"

    # Initialize Go module
    go mod init "$project_name"

    # Create main.go
    cat > main.go << EOF
package main

import (
    "fmt"
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello from $project_name!")
    })

    fmt.Println("Server starting on :8080...")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
EOF

    # Create go.mod (already created by go mod init, but let's ensure it has content)
    cat > go.mod << EOF
module $project_name

go 1.21
EOF

    # Create README
    cat > README.md << EOF
# $project_name

A Go project created with QWCoder.

## Getting Started

1. Initialize and download dependencies:
   \`\`\`bash
   go mod tidy
   \`\`\`

2. Run the application:
   \`\`\`bash
   go run main.go
   \`\`\`

3. Build the application:
   \`\`\`bash
   go build -o bin/app main.go
   \`\`\`

4. Run tests:
   \`\`\`bash
   go test ./...
   \`\`\`

## Available Commands

- \`go run main.go\` - Run application
- \`go build\` - Build application
- \`go test ./...\` - Run all tests
- \`go mod tidy\` - Clean up dependencies
- \`go fmt ./...\` - Format code

## Project Structure

\`\`\`
$project_name/
├── main.go          # Main application file
├── go.mod           # Go module file
├── go.sum           # Dependency checksums
└── README.md        # This file
\`\`\`
EOF

    # Create .gitignore
    cat > .gitignore << EOF
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with \`go test -c\`
*.test

# Output of the go coverage tool
*.out

# Go workspace file
go.work

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF

    log_success "Go project '$project_name' created successfully!"
    log_info "Next steps:"
    log_info "  cd $project_name"
    log_info "  go mod tidy"
    log_info "  go run main.go"
}

# Main function
main() {
    local project_type="$1"
    local project_name="$2"
    local template="${3:-basic}"

    if [ -z "$project_type" ] || [ -z "$project_name" ]; then
        echo "Usage: $0 <type> <name> [template]"
        echo ""
        echo "Project Types:"
        echo "  nodejs     - Node.js project"
        echo "  python     - Python project"
        echo "  react      - React.js project"
        echo "  go         - Go project"
        echo ""
        echo "Examples:"
        echo "  $0 nodejs my-api"
        echo "  $0 python data-analyzer"
        echo "  $0 react my-app"
        echo "  $0 go web-server"
        return 1
    fi

    # Check if directory already exists
    if [ -d "$project_name" ]; then
        log_error "Directory '$project_name' already exists!"
        return 1
    fi

    case "$project_type" in
        nodejs|node)
            create_nodejs_project "$project_name" "$template"
            ;;
        python|py)
            create_python_project "$project_name" "$template"
            ;;
        react)
            create_react_project "$project_name" "$template"
            ;;
        go)
            create_go_project "$project_name" "$template"
            ;;
        *)
            log_error "Unknown project type: $project_type"
            echo "Available types: nodejs, python, react, go"
            return 1
            ;;
    esac
}

# Run main function
main "$@"
