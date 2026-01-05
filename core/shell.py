# core/shell.py
import os
import sys
import subprocess

try:
    from prompt_toolkit import print_formatted_text as printf
    from prompt_toolkit.formatted_text import HTML
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False
    printf = print

def shell(cmd):
    """
    Execute commands with green output
    """
    if not cmd or cmd.strip() == "":
        return
    
    # Special handling for clear command
    if cmd.strip().lower() in ["clear", "cls"]:
        os.system('clear' if os.name != 'nt' else 'cls')
        return
    
    # Show command in green
    if HAS_PROMPT_TOOLKIT:
        printf(HTML(f'<style fg="green">$ {cmd}</style>'))
    else:
        print(f"\033[92m$ {cmd}\033[0m")  # ANSI green
    
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
        
        # Read output line by line and show in green
        for line in iter(process.stdout.readline, ''):
            if line:
                if HAS_PROMPT_TOOLKIT:
                    printf(HTML(f'<style fg="green">{line}</style>'), end="")
                else:
                    print(f"\033[92m{line}\033[0m", end="")
        
        process.wait()
        
    except Exception as e:
        # If subprocess fails, use os.system as fallback
        if HAS_PROMPT_TOOLKIT:
            printf(HTML(f'<style fg="red">Error: {str(e)}</style>'))
        else:
            print(f"\033[91mError: {str(e)}\033[0m")
        os.system(cmd)