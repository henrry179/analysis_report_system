#!/bin/bash

# QWCoder Setup Script
# This script sets up the QWCoder terminal environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QWCODER_HOME="$(cd "$SCRIPT_DIR/.." && pwd)"

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

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux" ;;
        Darwin*)    echo "macos" ;;
        CYGWIN*)    echo "cygwin" ;;
        MINGW*)     echo "mingw" ;;
        *)          echo "unknown" ;;
    esac
}

# Setup environment variables
setup_environment() {
    log_info "Setting up environment variables..."

    # Create .env file if it doesn't exist
    if [ ! -f "$QWCODER_HOME/.env" ]; then
        cp "$QWCODER_HOME/config/environment.env" "$QWCODER_HOME/.env"
        log_success "Created .env file"
    else
        log_warning ".env file already exists"
    fi

    # Export QWCODER_HOME
    export QWCODER_HOME="$QWCODER_HOME"

    log_success "Environment variables configured"
}

# Setup shell configuration
setup_shell() {
    local shell_type="$1"
    local shell_config=""

    case "$shell_type" in
        bash)
            shell_config="$HOME/.bashrc"
            source_config="$QWCODER_HOME/config/bashrc"
            ;;
        zsh)
            shell_config="$HOME/.zshrc"
            source_config="$QWCODER_HOME/config/zshrc"
            ;;
        *)
            log_error "Unsupported shell: $shell_type"
            return 1
            ;;
    esac

    log_info "Setting up $shell_type configuration..."

    # Create backup
    if [ -f "$shell_config" ]; then
        cp "$shell_config" "$shell_config.backup.$(date +%Y%m%d_%H%M%S)"
        log_info "Created backup of $shell_config"
    fi

    # Add QWCoder source line if not already present
    if ! grep -q "QWCoder" "$shell_config" 2>/dev/null; then
        echo "" >> "$shell_config"
        echo "# QWCoder Terminal Environment" >> "$shell_config"
        echo "export QWCODER_HOME=\"$QWCODER_HOME\"" >> "$shell_config"
        echo "source \"$source_config\"" >> "$shell_config"
        log_success "$shell_type configuration updated"
    else
        log_warning "QWCoder already configured in $shell_config"
    fi
}

# Install dependencies
install_dependencies() {
    local os=$(detect_os)

    log_info "Installing dependencies for $os..."

    case "$os" in
        linux)
            if command_exists apt-get; then
                log_info "Installing dependencies with apt-get..."
                sudo apt-get update
                sudo apt-get install -y curl wget git vim tree htop jq
            elif command_exists yum; then
                log_info "Installing dependencies with yum..."
                sudo yum install -y curl wget git vim tree htop jq
            elif command_exists pacman; then
                log_info "Installing dependencies with pacman..."
                sudo pacman -S --noconfirm curl wget git vim tree htop jq
            else
                log_warning "Package manager not found. Please install dependencies manually."
            fi
            ;;
        macos)
            if command_exists brew; then
                log_info "Installing dependencies with Homebrew..."
                brew install curl wget git vim tree htop jq
            else
                log_warning "Homebrew not found. Please install Homebrew and dependencies manually."
            fi
            ;;
        *)
            log_warning "Unsupported OS: $os. Please install dependencies manually."
            ;;
    esac

    log_success "Dependencies installation completed"
}

# Setup Git integration
setup_git_integration() {
    log_info "Setting up Git integration..."

    # Create git-integration.sh if it doesn't exist
    if [ ! -f "$QWCODER_HOME/config/git-integration.sh" ]; then
        cat > "$QWCODER_HOME/config/git-integration.sh" << 'EOF'
# Git Integration for QWCoder

# Git prompt
if [ -f "/usr/lib/git-core/git-sh-prompt" ]; then
    source "/usr/lib/git-core/git-sh-prompt"
    export PS1='\u@\h \w $(__git_ps1 "(%s)") $ '
elif [ -f "/usr/share/git/completion/git-prompt.sh" ]; then
    source "/usr/share/git/completion/git-prompt.sh"
    export PS1='\u@\h \w $(__git_ps1 "(%s)") $ '
fi

# Git aliases
alias gst='git status'
alias gco='git checkout'
alias gci='git commit'
alias grb='git rebase'
alias gbr='git branch'
alias glg='git log --oneline --graph --decorate'
alias gdf='git diff'
alias gad='git add'
alias gpl='git pull'
alias gps='git push'

# Git functions
gac() {
    git add . && git commit -m "$1"
}

gacp() {
    git add . && git commit -m "$1" && git push
}

gcb() {
    git checkout -b "$1"
}

gcm() {
    git checkout master || git checkout main
}
EOF
        log_success "Git integration configured"
    else
        log_warning "Git integration already exists"
    fi
}

# Setup custom functions
setup_functions() {
    log_info "Setting up custom functions..."

    # Create functions.sh if it doesn't exist
    if [ ! -f "$QWCODER_HOME/scripts/functions.sh" ]; then
        cat > "$QWCODER_HOME/scripts/functions.sh" << 'EOF'
# Custom Functions for QWCoder

# Extract archives
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
    grep -r "$1" . --exclude-dir=.git --exclude-dir=node_modules 2>/dev/null
}

# Show disk usage
duh() {
    du -h "$@" | sort -hr | head -10
}

# Process management
psgrep() {
    ps aux | grep "$1" | grep -v grep
}

# Network tools
myip() {
    curl -s ifconfig.me
}

weather() {
    curl wttr.in/"$1"
}

# Development helpers
serve() {
    local port="${1:-8000}"
    python3 -m http.server "$port"
}

jsonpp() {
    python3 -m json.tool
}

# System info
sysinfo() {
    echo "=== System Information ==="
    uname -a
    echo ""
    echo "=== CPU Info ==="
    nproc
    echo ""
    echo "=== Memory Info ==="
    free -h
    echo ""
    echo "=== Disk Usage ==="
    df -h
}
EOF
        log_success "Custom functions configured"
    else
        log_warning "Functions file already exists"
    fi
}

# Create bin directory executables
setup_bin() {
    log_info "Setting up binary scripts..."

    # Create qwcoder command
    cat > "$QWCODER_HOME/bin/qwcoder" << EOF
#!/bin/bash
# QWCoder main command

case "\$1" in
    setup)
        "$QWCODER_HOME/scripts/setup.sh"
        ;;
    update)
        "$QWCODER_HOME/scripts/update.sh"
        ;;
    help|*)
        "$QWCODER_HOME/scripts/help.sh"
        ;;
esac
EOF
    chmod +x "$QWCODER_HOME/bin/qwcoder"

    log_success "Binary scripts configured"
}

# Main setup function
main() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                      QWCoder Setup                           ║"
    echo "║                    Terminal Environment                      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    log_info "Starting QWCoder setup..."
    log_info "QWCoder Home: $QWCODER_HOME"

    # Detect shell
    local current_shell=$(basename "$SHELL")
    log_info "Detected shell: $current_shell"

    # Setup components
    setup_environment
    setup_shell "$current_shell"
    install_dependencies
    setup_git_integration
    setup_functions
    setup_bin

    echo ""
    log_success "QWCoder setup completed!"
    echo ""
    echo "Next steps:"
    echo "1. Restart your terminal or run: source ~/.${current_shell}rc"
    echo "2. Run 'qwcoder help' to see available commands"
    echo "3. Customize your configuration in $QWCODER_HOME/config/"
    echo ""
    echo "Happy coding with QWCoder! 🚀"
}

# Run main function
main "$@"
