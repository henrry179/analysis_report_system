# Custom Functions for QWCoder Terminal Environment

# Extract various archive formats
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2) tar xjf "$1" ;;
            *.tar.gz)  tar xzf "$1" ;;
            *.bz2)     bunzip2 "$1" ;;
            *.rar)     unrar x "$1" ;;
            *.gz)      gunzip "$1" ;;
            *.tar)     tar xf "$1" ;;
            *.tbz2)    tar xjf "$1" ;;
            *.tgz)     tar xzf "$1" ;;
            *.zip)     unzip "$1" ;;
            *.Z)       uncompress "$1" ;;
            *.7z)      7z x "$1" ;;
            *)         echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# Create directory and cd into it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Find file by name
ff() {
    find . -name "*$1*" 2>/dev/null
}

# Find file by content
fc() {
    grep -r "$1" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist --exclude-dir=build 2>/dev/null
}

# Show disk usage with human readable format
duh() {
    du -h "$@" | sort -hr | head -20
}

# Process management - find processes by name
psgrep() {
    ps aux | grep "$1" | grep -v grep
}

# Kill processes by name
pkill() {
    local process_name="$1"
    if [ -z "$process_name" ]; then
        echo "Usage: pkill <process_name>"
        return 1
    fi

    local pids=$(pgrep -f "$process_name")
    if [ -z "$pids" ]; then
        echo "No processes found with name: $process_name"
        return 1
    fi

    echo "Found processes:"
    ps -p $pids -o pid,ppid,cmd
    echo ""
    read -p "Kill these processes? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill $pids
        echo "Processes killed"
    fi
}

# Network tools
myip() {
    # Try multiple services for better reliability
    local ip_services=(
        "https://api.ipify.org"
        "https://ipv4.icanhazip.com"
        "https://checkip.amazonaws.com"
        "https://ipinfo.io/ip"
    )

    for service in "${ip_services[@]}"; do
        if command -v curl >/dev/null 2>&1; then
            local ip=$(curl -s --max-time 5 "$service" 2>/dev/null)
            if [ $? -eq 0 ] && [ -n "$ip" ]; then
                echo "$ip"
                return 0
            fi
        fi
    done

    echo "Unable to determine public IP"
    return 1
}

# Weather information
weather() {
    local city="${1:-}"
    if [ -z "$city" ]; then
        city=""
    fi

    if command -v curl >/dev/null 2>&1; then
        curl -s "wttr.in/$city" 2>/dev/null || echo "Weather service unavailable"
    else
        echo "curl not found. Please install curl to use weather function"
    fi
}

# Start HTTP server
serve() {
    local port="${1:-8000}"
    local dir="${2:-.}"

    if command -v python3 >/dev/null 2>&1; then
        echo "Starting HTTP server on port $port in directory: $dir"
        cd "$dir"
        python3 -m http.server "$port"
    elif command -v python >/dev/null 2>&1; then
        echo "Starting HTTP server on port $port in directory: $dir"
        cd "$dir"
        python -m SimpleHTTPServer "$port"
    elif command -v php >/dev/null 2>&1; then
        echo "Starting PHP server on port $port in directory: $dir"
        cd "$dir"
        php -S "localhost:$port"
    else
        echo "No suitable server found (python3, python, or php required)"
        return 1
    fi
}

# Pretty print JSON
jsonpp() {
    if [ -t 0 ]; then
        # File input
        if [ $# -eq 0 ]; then
            echo "Usage: jsonpp <file> or pipe JSON data"
            return 1
        fi
        python3 -m json.tool "$1"
    else
        # Pipe input
        python3 -m json.tool
    fi
}

# URL encode/decode
urlencode() {
    if [ -t 0 ]; then
        # File input
        if [ $# -eq 0 ]; then
            echo "Usage: urlencode <string> or pipe data"
            return 1
        fi
        python3 -c "import sys, urllib.parse; print(urllib.parse.quote('$1'))"
    else
        # Pipe input
        python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read()))"
    fi
}

urldecode() {
    if [ -t 0 ]; then
        # File input
        if [ $# -eq 0 ]; then
            echo "Usage: urldecode <string> or pipe data"
            return 1
        fi
        python3 -c "import sys, urllib.parse; print(urllib.parse.unquote('$1'))"
    else
        # Pipe input
        python3 -c "import sys, urllib.parse; print(urllib.parse.unquote(sys.stdin.read()))"
    fi
}

# System information
sysinfo() {
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                      System Information                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""

    echo "📅 Date & Time:"
    date
    echo ""

    echo "🖥️  OS Information:"
    uname -a
    echo ""

    if command -v lsb_release >/dev/null 2>&1; then
        echo "🐧 Distribution:"
        lsb_release -a 2>/dev/null
        echo ""
    fi

    echo "⚡ CPU Information:"
    if [ -f /proc/cpuinfo ]; then
        grep -E "model name|cpu cores|siblings" /proc/cpuinfo | head -3
    else
        echo "CPU cores: $(nproc 2>/dev/null || echo 'Unknown')"
    fi
    echo ""

    echo "🧠 Memory Information:"
    if command -v free >/dev/null 2>&1; then
        free -h
    else
        echo "Memory info not available"
    fi
    echo ""

    echo "💾 Disk Usage:"
    df -h | head -10
    echo ""

    echo "🌐 Network Interfaces:"
    if command -v ip >/dev/null 2>&1; then
        ip -brief addr show
    elif command -v ifconfig >/dev/null 2>&1; then
        ifconfig | grep -E "^[a-zA-Z]" | cut -d' ' -f1
    else
        echo "Network info not available"
    fi
    echo ""

    echo "🔧 Shell Information:"
    echo "Shell: $SHELL"
    echo "User: $(whoami)"
    echo "Home: $HOME"
    echo ""

    if [ -n "$QWCODER_HOME" ]; then
        echo "🚀 QWCoder Information:"
        echo "QWCoder Home: $QWCODER_HOME"
        echo "Version: $(cat "$QWCODER_HOME/config/qwcoder.json" 2>/dev/null | grep -o '"version": "[^"]*"' | cut -d'"' -f4 || echo 'Unknown')"
        echo ""
    fi
}

# Git utilities
git-stats() {
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                        Git Statistics                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""

    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        echo "Not a git repository"
        return 1
    fi

    echo "📊 Repository Statistics:"
    echo "Commits: $(git rev-list --count HEAD)"
    echo "Contributors: $(git shortlog -sn --no-merges | wc -l)"
    echo "Branches: $(git branch -a | wc -l)"
    echo "Tags: $(git tag | wc -l)"
    echo ""

    echo "📝 Recent Activity:"
    git log --oneline -10
    echo ""

    echo "📁 File Changes:"
    git diff --stat HEAD~1 2>/dev/null || echo "No previous commits to compare"
    echo ""

    echo "🔍 Uncommitted Changes:"
    if [ -n "$(git status --porcelain)" ]; then
        git status --short
    else
        echo "Working directory is clean"
    fi
}

# Docker utilities
docker-clean() {
    echo "🧹 Cleaning Docker..."
    echo ""

    echo "Stopping all containers..."
    docker stop $(docker ps -aq) 2>/dev/null || echo "No running containers"

    echo "Removing all containers..."
    docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"

    echo "Removing dangling images..."
    docker image prune -f

    echo "Removing unused volumes..."
    docker volume prune -f

    echo "Removing unused networks..."
    docker network prune -f

    echo ""
    echo "✅ Docker cleanup completed!"
}

# Development helpers
create-project() {
    local project_type="$1"
    local project_name="$2"

    if [ -z "$project_type" ] || [ -z "$project_name" ]; then
        echo "Usage: create-project <type> <name>"
        echo "Types: node, python, go, rust, react, vue, angular"
        return 1
    fi

    case "$project_type" in
        node)
            mkcd "$project_name"
            npm init -y
            echo "node_modules/" > .gitignore
            ;;
        python)
            mkcd "$project_name"
            python3 -m venv venv
            echo "venv/" > .gitignore
            echo "__pycache__/" >> .gitignore
            ;;
        go)
            mkcd "$project_name"
            go mod init "$project_name"
            ;;
        rust)
            if command -v cargo >/dev/null 2>&1; then
                cargo new "$project_name"
                cd "$project_name"
            else
                echo "Cargo not found. Please install Rust first."
                return 1
            fi
            ;;
        react)
            if command -v npx >/dev/null 2>&1; then
                npx create-react-app "$project_name"
                cd "$project_name"
            else
                echo "npx not found. Please install Node.js first."
                return 1
            fi
            ;;
        vue)
            if command -v npx >/dev/null 2>&1; then
                npx @vue/cli create "$project_name"
                cd "$project_name"
            else
                echo "npx not found. Please install Node.js first."
                return 1
            fi
            ;;
        angular)
            if command -v npx >/dev/null 2>&1; then
                npx @angular/cli new "$project_name"
                cd "$project_name"
            else
                echo "npx not found. Please install Node.js first."
                return 1
            fi
            ;;
        *)
            echo "Unknown project type: $project_type"
            echo "Available types: node, python, go, rust, react, vue, angular"
            return 1
            ;;
    esac

    echo "✅ Project '$project_name' created successfully!"
}

# Backup utilities
backup() {
    local source="$1"
    local dest="${2:-$HOME/backups/$(date +%Y%m%d_%H%M%S)}"

    if [ -z "$source" ]; then
        echo "Usage: backup <source> [destination]"
        return 1
    fi

    mkdir -p "$dest"
    cp -r "$source" "$dest/"

    echo "✅ Backup created: $dest"
}

# Timer function
timer() {
    local duration="$1"

    if [ -z "$duration" ]; then
        echo "Usage: timer <duration>"
        echo "Examples: timer 5m, timer 1h30m, timer 90s"
        return 1
    fi

    echo "⏰ Timer started for $duration"
    sleep "$duration"
    echo "⏰ Time's up!"
    # Try to make a sound if possible
    echo -e '\a' 2>/dev/null || tput bel 2>/dev/null || true
}

# Calculator
calc() {
    if [ $# -eq 0 ]; then
        echo "Usage: calc <expression>"
        echo "Examples: calc 2+2, calc 'sqrt(16)', calc 'sin(3.14/2)'"
        return 1
    fi

    python3 -c "import math; print(eval('$*', {'__builtins__': {}, 'math': math}))"
}

# Quick note taking
note() {
    local note_file="$HOME/notes.txt"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    if [ $# -eq 0 ]; then
        if [ -f "$note_file" ]; then
            echo "📝 Your notes:"
            cat "$note_file"
        else
            echo "No notes found. Use 'note <text>' to add a note."
        fi
        return 0
    fi

    echo "[$timestamp] $*" >> "$note_file"
    echo "✅ Note added!"
}

# File encryption/decryption
encrypt-file() {
    if [ $# -lt 1 ]; then
        echo "Usage: encrypt-file <file>"
        return 1
    fi

    if command -v gpg >/dev/null 2>&1; then
        gpg -c "$1"
        echo "✅ File encrypted: $1.gpg"
    else
        echo "GPG not found. Please install GPG to use encryption."
        return 1
    fi
}

decrypt-file() {
    if [ $# -lt 1 ]; then
        echo "Usage: decrypt-file <file.gpg>"
        return 1
    fi

    if command -v gpg >/dev/null 2>&1; then
        gpg "$1"
        echo "✅ File decrypted"
    else
        echo "GPG not found. Please install GPG to use decryption."
        return 1
    fi
}
