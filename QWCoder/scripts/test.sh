#!/bin/bash

# QWCoder Test Script
# Tests the QWCoder environment setup

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

# Test functions
test_file_exists() {
    local file="$1"
    if [ -f "$file" ]; then
        log_success "✓ $file exists"
        return 0
    else
        log_error "✗ $file missing"
        return 1
    fi
}

test_directory_exists() {
    local dir="$1"
    if [ -d "$dir" ]; then
        log_success "✓ $dir directory exists"
        return 0
    else
        log_error "✗ $dir directory missing"
        return 1
    fi
}

test_executable() {
    local file="$1"
    if [ -x "$file" ]; then
        log_success "✓ $file is executable"
        return 0
    else
        log_warning "⚠ $file is not executable"
        return 1
    fi
}

test_json_syntax() {
    local file="$1"
    if command -v python3 >/dev/null 2>&1; then
        if python3 -m json.tool "$file" >/dev/null 2>&1; then
            log_success "✓ $file has valid JSON syntax"
            return 0
        else
            log_error "✗ $file has invalid JSON syntax"
            return 1
        fi
    else
        log_warning "⚠ python3 not found, skipping JSON validation"
        return 0
    fi
}

test_shell_syntax() {
    local file="$1"
    if command -v bash >/dev/null 2>&1; then
        if bash -n "$file" 2>/dev/null; then
            log_success "✓ $file has valid shell syntax"
            return 0
        else
            log_error "✗ $file has invalid shell syntax"
            return 1
        fi
    else
        log_warning "⚠ bash not found, skipping shell syntax validation"
        return 0
    fi
}

# Main test function
main() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                     QWCoder Test Suite                       ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    local errors=0
    local warnings=0

    log_info "Starting QWCoder environment tests..."
    echo ""

    # Test directory structure
    log_info "Testing directory structure..."

    local dirs=("config" "scripts" "tools" "bin" "docs" "templates")
    for dir in "${dirs[@]}"; do
        if ! test_directory_exists "$dir"; then
            ((errors++))
        fi
    done

    echo ""

    # Test configuration files
    log_info "Testing configuration files..."

    local config_files=(
        "config/qwcoder.json"
        "config/environment.env"
        "config/aliases.sh"
        "config/bashrc"
    )

    for file in "${config_files[@]}"; do
        if ! test_file_exists "$file"; then
            ((errors++))
        fi
    done

    # Test JSON files
    test_json_syntax "config/qwcoder.json" || ((errors++))

    # Test shell files
    test_shell_syntax "config/aliases.sh" || ((errors++))
    test_shell_syntax "config/bashrc" || ((errors++))

    echo ""

    # Test script files
    log_info "Testing script files..."

    local script_files=(
        "scripts/setup.sh"
        "scripts/update.sh"
        "scripts/help.sh"
        "scripts/functions.sh"
        "scripts/test.sh"
    )

    for file in "${script_files[@]}"; do
        if ! test_file_exists "$file"; then
            ((errors++))
        fi
        if ! test_executable "$file"; then
            ((warnings++))
        fi
    done

    # Test shell syntax for scripts
    for file in "${script_files[@]}"; do
        if [ -f "$file" ]; then
            test_shell_syntax "$file" || ((errors++))
        fi
    done

    echo ""

    # Test tool files
    log_info "Testing tool files..."

    local tool_files=(
        "tools/package-manager.sh"
        "tools/project-templates.sh"
    )

    for file in "${tool_files[@]}"; do
        if ! test_file_exists "$file"; then
            ((errors++))
        fi
        if ! test_executable "$file"; then
            ((warnings++))
        fi
    done

    # Test shell syntax for tools
    for file in "${tool_files[@]}"; do
        if [ -f "$file" ]; then
            test_shell_syntax "$file" || ((errors++))
        fi
    done

    echo ""

    # Test documentation files
    log_info "Testing documentation files..."

    local doc_files=(
        "README.md"
        "docs/INSTALL.md"
        "docs/USAGE.md"
    )

    for file in "${doc_files[@]}"; do
        if ! test_file_exists "$file"; then
            ((errors++))
        fi
    done

    echo ""

    # Summary
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                        Test Summary                          ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    if [ $errors -eq 0 ]; then
        log_success "All tests passed! ✅"
        if [ $warnings -gt 0 ]; then
            log_warning "$warnings warnings found (non-critical)"
        fi
        echo ""
        echo "🎉 QWCoder environment is ready!"
        echo ""
        echo "Next steps:"
        echo "1. Run: ./scripts/setup.sh"
        echo "2. Restart your terminal"
        echo "3. Run: qwcoder help"
        echo ""
        return 0
    else
        log_error "$errors errors found"
        if [ $warnings -gt 0 ]; then
            log_warning "$warnings warnings found"
        fi
        echo ""
        log_error "Please fix the errors before proceeding."
        echo ""
        echo "Common fixes:"
        echo "- Make scripts executable: chmod +x scripts/*.sh tools/*.sh"
        echo "- Check file permissions and ownership"
        echo "- Verify all files were created correctly"
        echo ""
        return 1
    fi
}

# Run main function
main "$@"
