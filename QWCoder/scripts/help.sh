#!/bin/bash

# QWCoder Help Script
# Displays help information for QWCoder

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QWCODER_HOME="$(cd "$SCRIPT_DIR/.." && pwd)"

# Help sections
show_header() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                      QWCoder Help                            ║"
    echo "║                    Terminal Environment                      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
}

show_quick_start() {
    echo -e "${CYAN}QUICK START${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. Setup QWCoder:"
    echo -e "   ${GREEN}./scripts/setup.sh${NC}"
    echo ""
    echo "2. Restart your terminal or reload configuration:"
    echo -e "   ${GREEN}source ~/.bashrc${NC}  (for Bash)"
    echo -e "   ${GREEN}source ~/.zshrc${NC}   (for Zsh)"
    echo ""
    echo "3. Verify installation:"
    echo -e "   ${GREEN}qwcoder help${NC}"
    echo ""
}

show_commands() {
    echo -e "${CYAN}AVAILABLE COMMANDS${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${YELLOW}qwcoder setup${NC}     - Initial setup of QWCoder environment"
    echo -e "${YELLOW}qwcoder update${NC}    - Update QWCoder to latest version"
    echo -e "${YELLOW}qwcoder help${NC}      - Show this help information"
    echo ""
    echo -e "${YELLOW}qwconfig${NC}          - Edit QWCoder configuration"
    echo -e "${YELLOW}qwupdate${NC}          - Update QWCoder (alias)"
    echo -e "${YELLOW}qwhelp${NC}            - Show help (alias)"
    echo -e "${YELLOW}qwc${NC}               - Go to QWCoder home directory"
    echo ""
}

show_aliases() {
    echo -e "${CYAN}USEFUL ALIASES${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${GREEN}Navigation:${NC}"
    echo "  ..     - Go up one directory"
    echo "  ...    - Go up two directories"
    echo "  qwc    - Go to QWCoder home"
    echo ""
    echo -e "${GREEN}Git:${NC}"
    echo "  gs     - git status"
    echo "  ga     - git add"
    echo "  gcm    - git commit -m"
    echo "  gp     - git push"
    echo "  gl     - git log (graph)"
    echo ""
    echo -e "${GREEN}Docker:${NC}"
    echo "  d      - docker"
    echo "  dc     - docker-compose"
    echo "  dcu    - docker-compose up"
    echo "  dps    - docker ps"
    echo ""
    echo -e "${GREEN}Node.js:${NC}"
    echo "  n      - npm"
    echo "  ni     - npm install"
    echo "  ns     - npm start"
    echo "  nt     - npm test"
    echo ""
    echo -e "${GREEN}Python:${NC}"
    echo "  py     - python3"
    echo "  pip    - python3 -m pip"
    echo "  pi     - pip install"
    echo "  venv   - python3 -m venv"
    echo ""
}

show_functions() {
    echo -e "${CYAN}CUSTOM FUNCTIONS${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${YELLOW}extract <file>${NC}    - Extract various archive formats"
    echo -e "${YELLOW}mkcd <dir>${NC}        - Create directory and cd into it"
    echo -e "${YELLOW}ff <pattern>${NC}      - Find files by name"
    echo -e "${YELLOW}fc <pattern>${NC}      - Find files by content"
    echo -e "${YELLOW}duh${NC}               - Show disk usage (human readable)"
    echo -e "${YELLOW}psgrep <name>${NC}     - Find processes by name"
    echo -e "${YELLOW}myip${NC}              - Show your public IP"
    echo -e "${YELLOW}weather <city>${NC}    - Show weather information"
    echo -e "${YELLOW}serve [port]${NC}      - Start HTTP server (default port 8000)"
    echo -e "${YELLOW}jsonpp${NC}            - Pretty print JSON"
    echo -e "${YELLOW}sysinfo${NC}           - Show system information"
    echo ""
}

show_configuration() {
    echo -e "${CYAN}CONFIGURATION${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Main configuration file:"
    echo -e "  ${BLUE}$QWCODER_HOME/config/qwcoder.json${NC}"
    echo ""
    echo "Environment variables:"
    echo -e "  ${BLUE}$QWCODER_HOME/config/environment.env${NC}"
    echo ""
    echo "Shell configurations:"
    echo -e "  ${BLUE}$QWCODER_HOME/config/bashrc${NC}    (for Bash)"
    echo -e "  ${BLUE}$QWCODER_HOME/config/zshrc${NC}     (for Zsh)"
    echo ""
    echo "Aliases:"
    echo -e "  ${BLUE}$QWCODER_HOME/config/aliases.sh${NC}"
    echo ""
    echo "Custom functions:"
    echo -e "  ${BLUE}$QWCODER_HOME/scripts/functions.sh${NC}"
    echo ""
}

show_examples() {
    echo -e "${CYAN}EXAMPLES${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${GREEN}Edit configuration:${NC}"
    echo "  qwconfig"
    echo ""
    echo -e "${GREEN}Navigate to QWCoder:${NC}"
    echo "  qwc"
    echo ""
    echo -e "${GREEN}Update QWCoder:${NC}"
    echo "  qwupdate"
    echo ""
    echo -e "${GREEN}Extract a tar.gz file:${NC}"
    echo "  extract archive.tar.gz"
    echo ""
    echo -e "${GREEN}Create and enter directory:${NC}"
    echo "  mkcd myproject"
    echo ""
    echo -e "${GREEN}Find files containing 'TODO':${NC}"
    echo "  fc TODO"
    echo ""
    echo -e "${GREEN}Start development server:${NC}"
    echo "  serve 3000"
    echo ""
    echo -e "${GREEN}Check system info:${NC}"
    echo "  sysinfo"
    echo ""
}

show_troubleshooting() {
    echo -e "${CYAN}TROUBLESHOOTING${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${YELLOW}Configuration not loaded:${NC}"
    echo "  1. Restart your terminal"
    echo "  2. Check if QWCODER_HOME is set: echo \$QWCODER_HOME"
    echo "  3. Manually source config: source ~/.bashrc"
    echo ""
    echo -e "${YELLOW}Command not found:${NC}"
    echo "  1. Check PATH: echo \$PATH"
    echo "  2. Add QWCoder bin to PATH in your shell config"
    echo ""
    echo -e "${YELLOW}Permission denied:${NC}"
    echo "  1. Make scripts executable: chmod +x scripts/*.sh"
    echo "  2. Check file permissions: ls -la scripts/"
    echo ""
    echo -e "${YELLOW}Need to reset configuration:${NC}"
    echo "  1. Remove QWCoder lines from ~/.bashrc or ~/.zshrc"
    echo "  2. Run setup again: ./scripts/setup.sh"
    echo ""
}

show_support() {
    echo -e "${CYAN}SUPPORT${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "For issues and questions:"
    echo "• Check the troubleshooting section above"
    echo "• Review configuration files"
    echo "• Update to latest version: qwupdate"
    echo ""
    echo "Configuration files location:"
    echo -e "  ${BLUE}$QWCODER_HOME${NC}"
    echo ""
    echo -e "${GREEN}Happy coding with QWCoder! 🚀${NC}"
    echo ""
}

# Main help function
main() {
    case "$1" in
        quick|start)
            show_header
            show_quick_start
            ;;
        commands|cmds)
            show_header
            show_commands
            ;;
        aliases)
            show_header
            show_aliases
            ;;
        functions|funcs)
            show_header
            show_functions
            ;;
        config)
            show_header
            show_configuration
            ;;
        examples)
            show_header
            show_examples
            ;;
        troubleshoot|trouble)
            show_header
            show_troubleshooting
            ;;
        all|"")
            show_header
            show_quick_start
            show_commands
            show_aliases
            show_functions
            show_configuration
            show_examples
            show_troubleshooting
            show_support
            ;;
        *)
            echo -e "${RED}Unknown help topic: $1${NC}"
            echo ""
            echo "Available topics:"
            echo "  quick      - Quick start guide"
            echo "  commands   - Available commands"
            echo "  aliases    - Useful aliases"
            echo "  functions  - Custom functions"
            echo "  config     - Configuration files"
            echo "  examples   - Usage examples"
            echo "  troubleshoot - Troubleshooting guide"
            echo "  all        - Complete help (default)"
            ;;
    esac
}

# Run main function
main "$@"
