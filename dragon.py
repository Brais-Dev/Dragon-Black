"""
main file
"""
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from modules import banner
from modules import packages
from core import shell
from core.configuration_language import Translator
from core import updater
from core.command_handler import CommandHandler
from core.input_validator import validate_command
from datetime import datetime
from prompt_toolkit.completion import WordCompleter
from modules.prompt_manager import DragonPromptManager
from prompt_toolkit import prompt
import json
from core.plugin_manager import load_all_plugins

app = Translator()
console = Console()
banner.dots()

# Initialize other modules
os.system("clear")

# Obsolete route for the version file
dir_fil = Path(__file__).parent.parent / "Dragon-Black" / "data"
file = dir_fil / "version.txt"

# Read the file that handles the versions
with open(file, "r") as f:
    lines = [line for line in f]
for li in lines:
    panel = Panel(
      f"[blue]dragon: {li}[/blue]",
        width=20)
    console.print(panel)

# Initialize command handler
command_handler = CommandHandler()

# Load all plugins and register them with command handler
from core.plugin_manager import plugin_manager
plugin_manager.command_handler = command_handler
load_all_plugins()

# Initialize shell color (this ensures the color file exists and loads properly)
shell.get_shell_color()

# Suggestions on the screen
file_command = Path(__file__).parent.parent / "Dragon-Black" / "data"
options_command = file_command / "command.json"

# Load file that contains the autocomplete
with open(options_command, 'r', encoding='utf-8') as f:
    command = json.load(f)
prompt_manager = DragonPromptManager(command, theme="dragon")

# main loop
while True:
    cmd = prompt_manager.get_prompt()
    
    """
    handle customization commands from the main loop because Aki is where the prompt 
    """
    if cmd == "theme":
        # Interactive theme changer
        print("\nAvailable themes:")
        themes = prompt_manager.list_themes()
        for i, theme in enumerate(themes, 1):
            print(f"  [{i}] {theme}")
        
        try:
            choice = input("\nSelect theme (number): ")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(themes):
                    prompt_manager.change_theme(themes[idx])
                    print(f"✓ Theme changed to: {themes[idx]}")
        except:
            print("✗ Invalid selection")
        continue
    
    elif cmd == "theme list":
        themes = prompt_manager.list_themes()
        print("\nAvailable themes:")
        for theme in themes:
            print(f"  • {theme}")
        continue
    
    elif cmd.startswith("theme set "):
        theme_name = cmd.replace("theme set ", "").strip()
        if theme_name in prompt_manager.list_themes():
            prompt_manager.change_theme(theme_name)
            print(f"✓ Theme set to: {theme_name}")
        else:
            print(f"✗ Theme '{theme_name}' not found")
        continue
    
    elif cmd == "theme info":
        prompt_manager.show_theme_info()
        continue
    
    elif cmd == "autocomplete stats":
        stats = prompt_manager.get_stats()
        print(f"\nAutocomplete Statistics:")
        print(f"  Total commands: {stats['command_count']}")
        print(f"  Prompts shown: {stats['prompt_count']}")
        print(f"  Current theme: {stats['theme']}")
        print(f"  History entries: {stats['history_entries']}")
        continue
   
    # Validate command for security
    is_safe, reason = validate_command(cmd)
    if not is_safe:
        print(f"Command rejected: {reason}")
        continue

    # Handle command using the new command handler first
    result = command_handler.handle_command(cmd)

    # If command was handled by command handler, continue to next iteration
    if result is not None:
        if result == "exit":
            break
        continue
    else:
        # If command wasn't handled by command handler, execute it as shell command
        shell.shell(cmd)

    # exit program
    if cmd == "exit":
        break
