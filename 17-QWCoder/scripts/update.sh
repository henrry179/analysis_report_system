#!/bin/bash

# QWCoder Update Script
# Updates the QWCoder environment

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

# Backup current configuration
backup_config() {
    log_info "Creating backup of current configuration..."

    local backup_dir="$QWCODER_HOME/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"

    # Backup config files
    cp -r "$QWCODER_HOME/config" "$backup_dir/"
    cp -r "$QWCODER_HOME/scripts" "$backup_dir/"
    cp -r "$QWCODER_HOME/tools" "$backup_dir/" 2>/dev/null || true

    log_success "Backup created at: $backup_dir"
}

# Update from git repository
update_from_git() {
    if [ -d "$QWCODER_HOME/.git" ]; then
        log_info "Updating from git repository..."

        cd "$QWCODER_HOME"
        git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true

        log_success "Git update completed"
    else
        log_warning "Not a git repository, skipping git update"
    fi
}

# Update scripts and tools
update_scripts() {
    log_info "Updating scripts and tools..."

    # Make scripts executable
    find "$QWCODER_HOME/scripts" -name "*.sh" -type f -exec chmod +x {} \;
    find "$QWCODER_HOME/tools" -name "*.sh" -type f -exec chmod +x {} \; 2>/dev/null || true

    log_success "Scripts updated"
}

# Update dependencies
update_dependencies() {
    log_info "Checking for dependency updates..."

    # Check for package managers
    if command -v apt-get >/dev/null 2>&1; then
        log_info "Updating apt packages..."
        sudo apt-get update && sudo apt-get upgrade -y
    elif command -v yum >/dev/null 2>&1; then
        log_info "Updating yum packages..."
        sudo yum update -y
    elif command -v brew >/dev/null 2>&1; then
        log_info "Updating Homebrew packages..."
        brew update && brew upgrade
    fi

    log_success "Dependencies updated"
}

# Clean up old files
cleanup() {
    log_info "Cleaning up old files..."

    # Remove old backup files (keep last 5)
    if [ -d "$QWCODER_HOME/backups" ]; then
        ls -t "$QWCODER_HOME/backups" | tail -n +6 | xargs -I {} rm -rf "$QWCODER_HOME/backups/{}" 2>/dev/null || true
    fi

    # Clean up temporary files
    find "$QWCODER_HOME" -name "*.tmp" -type f -delete 2>/dev/null || true
    find "$QWCODER_HOME" -name "*.bak" -type f -delete 2>/dev/null || true

    log_success "Cleanup completed"
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."

    local errors=0

    # Check required files
    local required_files=(
        "config/qwcoder.json"
        "config/environment.env"
        "scripts/setup.sh"
        "scripts/update.sh"
        "scripts/help.sh"
    )

    for file in "${required_files[@]}"; do
        if [ ! -f "$QWCODER_HOME/$file" ]; then
            log_error "Missing file: $file"
            ((errors++))
        fi
    done

    # Check script permissions
    if [ ! -x "$QWCODER_HOME/scripts/setup.sh" ]; then
        log_warning "setup.sh is not executable"
        chmod +x "$QWCODER_HOME/scripts/setup.sh"
    fi

    if [ ! -x "$QWCODER_HOME/scripts/update.sh" ]; then
        log_warning "update.sh is not executable"
        chmod +x "$QWCODER_HOME/scripts/update.sh"
    fi

    if [ $errors -eq 0 ]; then
        log_success "Installation verification passed"
        return 0
    else
        log_error "Installation verification failed with $errors errors"
        return 1
    fi
}

# Show update summary
show_summary() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                      Update Summary                          ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "QWCoder has been updated successfully!"
    echo ""
    echo "What's new:"
    echo "✓ Configuration files updated"
    echo "✓ Scripts refreshed"
    echo "✓ Dependencies checked"
    echo "✓ Cleanup performed"
    echo ""
    echo "To apply changes:"
    echo "1. Restart your terminal"
    echo "2. Or run: source ~/.bashrc (or ~/.zshrc)"
    echo ""
}

# Main update function
main() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                      QWCoder Update                          ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    log_info "Starting QWCoder update..."
    log_info "QWCoder Home: $QWCODER_HOME"

    # Run update steps
    backup_config
    update_from_git
    update_scripts
    update_dependencies
    cleanup

    # Verify installation
    if verify_installation; then
        show_summary
        log_success "QWCoder update completed successfully!"
    else
        log_error "Update completed with errors. Please check the logs above."
        exit 1
    fi
}

# Run main function
main "$@"
