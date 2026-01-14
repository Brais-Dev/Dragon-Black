#!/bin/bash
set -e

# ===============================
# Dragon-Black Minimal Pro Termux
# ===============================

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
WHITE="\033[0m"

echo -e "${GREEN}[*] Setting up Dragon-Black professional shell...${WHITE}"

# -------------------------------
# Update system
# -------------------------------
yes | pkg update && yes | pkg upgrade

# -------------------------------
# Essential packages
# -------------------------------
yes | pkg install \
git \
zsh \
curl \
wget \
lsd \
bat \
fzf \
ripgrep \
ncurses-utils \
neovim \
python \
nodejs

# -------------------------------
# Install Oh My Zsh (no auto exec)
# -------------------------------
echo -e "${GREEN}[*] Installing Oh My Zsh...${WHITE}"

curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -o install.sh
sed -i '/exec zsh -l/s/^/#/' install.sh
sh install.sh
rm install.sh

# -------------------------------
# ZSH plugins directory
# -------------------------------
mkdir -p ~/.zsh-plugins

# -------------------------------
# Plugins
# -------------------------------
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
~/.zsh-plugins/powerlevel10k

git clone https://github.com/zsh-users/zsh-autosuggestions.git \
~/.zsh-plugins/zsh-autosuggestions

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
~/.zsh-plugins/zsh-syntax-highlighting

git clone https://github.com/zsh-users/zsh-history-substring-search.git \
~/.zsh-plugins/zsh-history-substring-search

git clone https://github.com/Aloxaf/fzf-tab.git \
~/.zsh-plugins/fzf-tab

# -------------------------------
# ZSH CONFIG (CORRECT ORDER)
# -------------------------------
cat > ~/.zshrc << 'EOF'
# ===============================
# Dragon-Black ZSH Configuration
# ===============================

# Enable completion system (REQUIRED)
autoload -Uz compinit
compinit

# Theme
source ~/.zsh-plugins/powerlevel10k/powerlevel10k.zsh-theme

# Autosuggestions (INLINE)
ZSH_AUTOSUGGEST_STRATEGY=(history completion)
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=8'
source ~/.zsh-plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# History substring search
source ~/.zsh-plugins/zsh-history-substring-search/zsh-history-substring-search.zsh
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# Better TAB completion
source ~/.zsh-plugins/fzf-tab/fzf-tab.plugin.zsh
zstyle ':fzf-tab:*' switch-group ',' '.'

# Syntax highlighting (MUST BE LAST)
source ~/.zsh-plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# Aliases
alias ls='lsd --icon=always'
alias ll='lsd -lah --icon=always'
alias tree='lsd --tree --icon=always'
alias cat='bat --theme=Dracula --style=plain --paging=never'

# Dragon-Black identity
export DRAGON_BLACK=1
export EDITOR=nvim

EOF

# -------------------------------
# Termux UI tweaks
# -------------------------------
mkdir -p ~/.termux

cat > ~/.termux/termux.properties << 'EOF'
terminal-cursor-blink-rate=500
extra-keys = [
 ['ESC','TAB','CTRL','ALT','HOME','UP','END','PGUP'],
 ['','', '', '', 'LEFT','DOWN','RIGHT','PGDN']
]
EOF

cat > ~/.termux/colors.properties << 'EOF'
cursor=#00FF00
EOF

# -------------------------------
# Install Nerd Font (Meslo)
# -------------------------------
echo -e "${GREEN}[*] Installing Nerd Font...${WHITE}"

curl -L -o ~/.termux/font.ttf \
https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf

# -------------------------------
# Finish
# -------------------------------
echo -e "${YELLOW}[!] Setup complete.${WHITE}"
echo -e "${YELLOW}[!] Restart Termux COMPLETELY.${WHITE}"
echo -e "${YELLOW}[!] Then run: dragon${WHITE}"