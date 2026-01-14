# core/shell.py
import os
import sys
import subprocess
from pathlib import Path

try:
    from prompt_toolkit import print_formatted_text as printf
    from prompt_toolkit.formatted_text import HTML
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False
    printf = print

# Define ANSI color codes
COLOR_CODES = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bright_black': '\033[90m',
    'bright_red': '\033[91m',
    'bright_green': '\033[92m',
    'bright_yellow': '\033[93m',
    'bright_blue': '\033[94m',
    'bright_magenta': '\033[95m',
    'bright_cyan': '\033[96m',
    'bright_white': '\033[97m',
}

RESET_COLOR = '\033[0m'

def get_shell_color():
    """Get the current shell color from the configuration file"""
    data_dir = Path(__file__).parent.parent / "data"
    color_file = data_dir / "shell_color.txt"

    if color_file.exists():
        with open(color_file, 'r') as f:
            color = f.read().strip()
            if color in COLOR_CODES:
                return color
    return 'white'  # Default color

def set_shell_color(color):
    """Set the shell color in the configuration file"""
    data_dir = Path(__file__).parent.parent / "data"
    color_file = data_dir / "shell_color.txt"

    if color in COLOR_CODES:
        with open(color_file, 'w') as f:
            f.write(color)
        return True
    return False

def shell(cmd):
    """
    Execute commands with configurable color output
    """
    if not cmd or cmd.strip() == "":
        return

    # Special handling for clear command
    if cmd.strip().lower() in ["clear", "cls"]:
        os.system('clear' if os.name != 'nt' else 'cls')
        return

    # Special handling for cd command - this needs to affect the parent process
    if cmd.strip().lower().startswith("cd"):
        try:
            # Extract the directory from the command
            parts = cmd.strip().split(" ", 1)
            if len(parts) > 1:
                directory = parts[1].strip()
            else:
                # If no argument is provided, go to home directory
                directory = os.path.expanduser("~")

            if directory == "" or directory == "~":
                directory = os.path.expanduser("~")
            elif directory == "-":
                # Go to previous directory
                directory = os.environ.get("OLDPWD", os.getcwd())

            # Store current directory before changing
            old_dir = os.getcwd()
            os.chdir(directory)

            # Update environment variable
            os.environ["OLDPWD"] = old_dir
            os.environ["PWD"] = os.getcwd()

            # Show command in selected color
            current_color = get_shell_color()
            if HAS_PROMPT_TOOLKIT:
                printf(HTML(f'<style fg="{current_color}">$ {cmd}</style>'))
            else:
                color_code = COLOR_CODES[current_color]
                print(f"{color_code}$ {cmd}{RESET_COLOR}")  # ANSI color
            print(f"Changed directory to: {os.getcwd()}")
            return
        except FileNotFoundError:
            current_color = get_shell_color()
            if HAS_PROMPT_TOOLKIT:
                printf(HTML(f'<style fg="red">cd: no such file or directory: {parts[1].strip() if len(parts) > 1 else "~"}</style>'))
            else:
                dir_arg = parts[1].strip() if len(parts) > 1 else "~"
                print(f"\033[91mcd: no such file or directory: {dir_arg}\033[0m")
            return
        except PermissionError:
            current_color = get_shell_color()
            if HAS_PROMPT_TOOLKIT:
                printf(HTML(f'<style fg="red">cd: permission denied: {parts[1].strip() if len(parts) > 1 else "~"}</style>'))
            else:
                dir_arg = parts[1].strip() if len(parts) > 1 else "~"
                print(f"\033[91mcd: permission denied: {dir_arg}\033[0m")
            return
        except Exception as e:
            current_color = get_shell_color()
            if HAS_PROMPT_TOOLKIT:
                printf(HTML(f'<style fg="red">cd: error: {str(e)}</style>'))
            else:
                print(f"\033[91mcd: error: {str(e)}\033[0m")
            return

    # Get current shell color
    current_color = get_shell_color()
    color_code = COLOR_CODES[current_color]

    # Show command in selected color
    if HAS_PROMPT_TOOLKIT:
        printf(HTML(f'<style fg="{current_color}">$ {cmd}</style>'))
    else:
        print(f"{color_code}$ {cmd}{RESET_COLOR}")  # ANSI color

    # Execute command
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Read output line by line and show in selected color
        for line in iter(process.stdout.readline, ''):
            if line:
                if HAS_PROMPT_TOOLKIT:
                    printf(HTML(f'<style fg="{current_color}">{line}</style>'), end="")
                else:
                    print(f"{color_code}{line}{RESET_COLOR}", end="")

        process.wait()

    except Exception as e:
        # If subprocess fails, use os.system as fallback
        if HAS_PROMPT_TOOLKIT:
            printf(HTML(f'<style fg="red">Error: {str(e)}</style>'))
        else:
            print(f"\033[91mError: {str(e)}\033[0m")
        os.system(cmd)

def change_shell_color(color):
    """
    Change the shell color and save it to the configuration file
    """
    if set_shell_color(color):
        current_color = get_shell_color()
        print(f"Shell color changed to {current_color}")
    else:
        print(f"Invalid color: {color}. Available colors: {', '.join(COLOR_CODES.keys())}")