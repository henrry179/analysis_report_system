#!/bin/bash

# QWCoder Package Manager Helper
# Helps manage various package managers and development tools

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

# Detect package manager
detect_package_manager() {
    if command -v apt-get >/dev/null 2>&1; then
        echo "apt"
    elif command -v yum >/dev/null 2>&1; then
        echo "yum"
    elif command -v dnf >/dev/null 2>&1; then
        echo "dnf"
    elif command -v pacman >/dev/null 2>&1; then
        echo "pacman"
    elif command -v zypper >/dev/null 2>&1; then
        echo "zypper"
    elif command -v brew >/dev/null 2>&1; then
        echo "brew"
    else
        echo "unknown"
    fi
}

# Update system packages
update_system() {
    local os=$(detect_os)
    local pm=$(detect_package_manager)

    log_info "Updating system packages ($os with $pm)..."

    case "$pm" in
        apt)
            sudo apt-get update && sudo apt-get upgrade -y
            ;;
        yum)
            sudo yum update -y
            ;;
        dnf)
            sudo dnf update -y
            ;;
        pacman)
            sudo pacman -Syu --noconfirm
            ;;
        zypper)
            sudo zypper update -y
            ;;
        brew)
            brew update && brew upgrade
            ;;
        *)
            log_warning "Unsupported package manager: $pm"
            return 1
            ;;
    esac

    log_success "System packages updated"
}

# Install development tools
install_dev_tools() {
    local os=$(detect_os)
    local pm=$(detect_package_manager)

    log_info "Installing development tools..."

    local tools=(
        curl wget git vim neovim tree htop jq
        build-essential cmake make gcc g++
        python3 python3-pip python3-venv
        nodejs npm
    )

    case "$pm" in
        apt)
            sudo apt-get install -y "${tools[@]}"
            ;;
        yum)
            sudo yum install -y "${tools[@]}"
            ;;
        dnf)
            sudo dnf install -y "${tools[@]}"
            ;;
        pacman)
            sudo pacman -S --noconfirm "${tools[@]}"
            ;;
        zypper)
            sudo zypper install -y "${tools[@]}"
            ;;
        brew)
            brew install "${tools[@]}"
            ;;
        *)
            log_warning "Unsupported package manager: $pm"
            return 1
            ;;
    esac

    log_success "Development tools installed"
}

# Setup Node.js with NVM
setup_nodejs() {
    log_info "Setting up Node.js with NVM..."

    if [ ! -d "$HOME/.nvm" ]; then
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
        log_success "NVM installed"
    else
        log_warning "NVM already installed"
    fi

    # Load NVM
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

    # Install latest LTS Node.js
    if command -v nvm >/dev/null 2>&1; then
        nvm install --lts
        nvm use --lts
        nvm alias default lts/*
        log_success "Node.js LTS installed and set as default"
    fi
}

# Setup Python tools
setup_python() {
    log_info "Setting up Python development tools..."

    # Install pip for Python 3
    if command -v python3 >/dev/null 2>&1; then
        python3 -m pip install --user --upgrade pip setuptools wheel

        # Install common Python packages
        python3 -m pip install --user \
            virtualenv virtualenvwrapper \
            pipenv poetry \
            black flake8 pylint mypy \
            jupyter notebook

        log_success "Python tools installed"
    else
        log_warning "Python3 not found"
    fi
}

# Setup Go
setup_go() {
    log_info "Setting up Go development environment..."

    local os=$(detect_os)
    local arch=$(uname -m)

    # Determine Go version and download URL
    local go_version="1.21.0"
    local go_url=""

    case "$os" in
        linux)
            case "$arch" in
                x86_64) go_url="https://go.dev/dl/go${go_version}.linux-amd64.tar.gz" ;;
                aarch64) go_url="https://go.dev/dl/go${go_version}.linux-arm64.tar.gz" ;;
                *) log_warning "Unsupported architecture: $arch"; return 1 ;;
            esac
            ;;
        macos)
            case "$arch" in
                x86_64) go_url="https://go.dev/dl/go${go_version}.darwin-amd64.tar.gz" ;;
                arm64) go_url="https://go.dev/dl/go${go_version}.darwin-arm64.tar.gz" ;;
                *) log_warning "Unsupported architecture: $arch"; return 1 ;;
            esac
            ;;
        *)
            log_warning "Go installation not supported for $os"
            return 1
            ;;
    esac

    if [ -n "$go_url" ]; then
        log_info "Downloading Go $go_version..."
        curl -L "$go_url" -o /tmp/go.tar.gz

        log_info "Installing Go..."
        sudo rm -rf /usr/local/go
        sudo tar -C /usr/local -xzf /tmp/go.tar.gz
        rm /tmp/go.tar.gz

        log_success "Go $go_version installed"
    fi
}

# Setup Docker
setup_docker() {
    local os=$(detect_os)

    log_info "Setting up Docker..."

    case "$os" in
        linux)
            # Install Docker using convenience script
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
            rm get-docker.sh
            ;;
        macos)
            if ! command -v brew >/dev/null 2>&1; then
                log_error "Homebrew not found. Please install Homebrew first."
                return 1
            fi
            brew install --cask docker
            ;;
        *)
            log_warning "Docker installation not supported for $os"
            return 1
            ;;
    esac

    log_success "Docker installed"
    log_info "Please restart your session to use Docker without sudo"
}

# Setup development editors
setup_editors() {
    log_info "Setting up development editors..."

    # VS Code
    if command -v code >/dev/null 2>&1; then
        log_warning "VS Code already installed"
    else
        local os=$(detect_os)
        case "$os" in
            linux)
                curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg
                echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
                sudo apt-get update
                sudo apt-get install -y code
                ;;
            macos)
                if command -v brew >/dev/null 2>&1; then
                    brew install --cask visual-studio-code
                fi
                ;;
        esac
        log_success "VS Code installed"
    fi
}

# Main function
main() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                 QWCoder Package Manager                      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    local command="$1"

    case "$command" in
        update)
            update_system
            ;;
        dev-tools)
            install_dev_tools
            ;;
        nodejs)
            setup_nodejs
            ;;
        python)
            setup_python
            ;;
        go)
            setup_go
            ;;
        docker)
            setup_docker
            ;;
        editors)
            setup_editors
            ;;
        all)
            update_system
            install_dev_tools
            setup_nodejs
            setup_python
            setup_go
            setup_docker
            setup_editors
            ;;
        *)
            echo "Usage: $0 <command>"
            echo ""
            echo "Commands:"
            echo "  update     - Update system packages"
            echo "  dev-tools  - Install development tools"
            echo "  nodejs     - Setup Node.js with NVM"
            echo "  python     - Setup Python tools"
            echo "  go         - Setup Go development environment"
            echo "  docker     - Setup Docker"
            echo "  editors    - Setup development editors"
            echo "  all        - Setup everything"
            ;;
    esac
}

# Run main function
main "$@"
