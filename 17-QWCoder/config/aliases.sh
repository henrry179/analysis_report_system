# QWCoder Aliases Configuration

# Navigation Aliases
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ~="cd ~"
alias qwc="cd $QWCODER_HOME"
alias dl="cd ~/Downloads"
alias dt="cd ~/Desktop"
alias doc="cd ~/Documents"

# QWCoder Specific Aliases
alias qwconfig="vim $QWCODER_HOME/config/qwcoder.json"
alias qwupdate="$QWCODER_HOME/scripts/update.sh"
alias qwhelp="$QWCODER_HOME/scripts/help.sh"
alias qwsetup="$QWCODER_HOME/scripts/setup.sh"

# List Commands
alias ls="ls --color=auto"
alias ll="ls -alF"
alias la="ls -A"
alias l="ls -CF"
alias dir="ls -l"
alias tree="tree -C"

# Git Aliases
alias gs="git status"
alias ga="git add"
alias gaa="git add --all"
alias gc="git commit"
alias gcm="git commit -m"
alias gca="git commit --amend"
alias gp="git push"
alias gpf="git push --force-with-lease"
alias gl="git log --oneline --graph --decorate"
alias gll="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
alias gd="git diff"
alias gds="git diff --staged"
alias gb="git branch"
alias gba="git branch -a"
alias gco="git checkout"
alias gcb="git checkout -b"
alias gm="git merge"
alias gr="git rebase"
alias gri="git rebase -i"
alias gf="git fetch"
alias gfa="git fetch --all"
alias gpl="git pull"
alias gplr="git pull --rebase"
alias gst="git stash"
alias gstp="git stash pop"
alias gstl="git stash list"

# Docker Aliases
alias d="docker"
alias dc="docker-compose"
alias dcu="docker-compose up"
alias dcd="docker-compose down"
alias dcb="docker-compose build"
alias dcl="docker-compose logs"
alias dclf="docker-compose logs -f"
alias dps="docker ps"
alias dpsa="docker ps -a"
alias di="docker images"
alias drm="docker rm"
alias drmi="docker rmi"
alias dv="docker volume"
alias dn="docker network"

# Node.js Aliases
alias n="npm"
alias ni="npm install"
alias nid="npm install --save-dev"
alias nig="npm install -g"
alias nr="npm run"
alias ns="npm start"
alias nt="npm test"
alias nb="npm run build"
alias nl="npm list"
alias nlg="npm list -g"

# Python Aliases
alias py="python3"
alias pip="python3 -m pip"
alias pi="python3 -m pip install"
alias pir="python3 -m pip install -r requirements.txt"
alias pf="pip freeze"
alias pfr="pip freeze > requirements.txt"
alias venv="python3 -m venv"
alias va="source venv/bin/activate"
alias vd="deactivate"

# System Aliases
alias cls="clear"
alias h="history"
alias j="jobs -l"
alias path="echo -e ${PATH//:/\\n}"
alias now="date +'%Y-%m-%d %H:%M:%S'"
alias weather="curl wttr.in"
alias myip="curl -s ifconfig.me"

# Development Aliases
alias serve="python3 -m http.server"
alias jsonpp="python3 -m json.tool"
alias urlencode="python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read()))'"
alias urldecode="python3 -c 'import sys, urllib.parse; print(urllib.parse.unquote(sys.stdin.read()))'"

# File Management
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"
alias mkdir="mkdir -p"
alias wget="wget -c"
alias grep="grep --color=auto"
alias egrep="egrep --color=auto"
alias fgrep="fgrep --color=auto"

# Network
alias ping="ping -c 5"
alias ports="netstat -tulanp"
alias speedtest="curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -"

# Security
alias encrypt="gpg -c --no-symkey-cache --cipher-algo AES256"
alias decrypt="gpg --no-symkey-cache"
