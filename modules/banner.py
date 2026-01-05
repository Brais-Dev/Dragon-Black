import time
import os
import sys
import random
import shutil
from colorama import init, Fore, Style

# Initialize colorama for terminal colors
init()

def dots():
    spinners = {
        "arrows": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
      #   "a": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
        
    }
    
    massages = [
        "Loading the system....",
        "Preparing the configuration files....",
        "The system is very big please wait .....",
        "please wait...",
        "Configuration initiated correctly",
    ]
    
    print("\033[1mDragon-Black\033[0m\n")
    
    for tipo_spinner in ["arrows"]:
        spinner = spinners[tipo_spinner]
        messg = massages[list(spinners.keys()).index(tipo_spinner) % len(massages)]
        
        for i in range(100):  # 20 ciclos por spinner
            frame = spinner[i % len(spinner)]
            
            # Color diferente según el estado
            if i < 5:
                color = "\033[31m"
            
            if i < 10:
                color = "\033[32m"
                
                
            if i < 20:
                color = "\033[33m"
            
            if i < 30:
                color = "\033[34m"
                
            if i < 40:
                color = "\033[35m"
           
            if i < 50:
                color = "\033[36m"
            else:
                color = "\033[37m"  # Verde
            
            sys.stdout.write(f"\r{color}{frame}\033[34m {messg} [{i+1}] ")
            sys.stdout.flush()
            time.sleep(0.1)
        
        print(f"\r√ {messg} System started correctly!          ") 
        time.sleep(2)
        break
        
        
       
       



def get_terminal_width():
    """Gets the current terminal width"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80  # Default width

def center_text(text, total_width):
    """Centers text in available width"""
    # Remove color codes for length calculation
    clean_text = text.replace(Fore.GREEN, '').replace(Fore.CYAN, '').replace(Fore.BLUE, '').replace(Fore.WHITE, '').replace(Style.BRIGHT, '').replace(Style.RESET_ALL, '')
    real_length = len(clean_text)
    spaces = max(0, (total_width - real_length) // 2)
    return " " * spaces + text

def create_frame(width):
    """Creates dynamic frame based on screen width"""
    if width < 60:
        # Compact version for small screens
        frame_top = "┌" + "─" * (width - 2) + "┐"
        frame_side = "│" + " " * (width - 2) + "│"
        frame_bottom = "└" + "─" * (width - 2) + "┘"
    else:
        # Full version for large screens
        frame_top = "╔" + "═" * (width - 2) + "╗"
        frame_side = "║" + " " * (width - 2) + "║"
        frame_bottom = "╚" + "═" * (width - 2) + "╝"
    
    return frame_top, frame_side, frame_bottom

def create_progress_bar(percentage, width):
    """Creates animated progress bar"""
    bar_length = min(40, width - 20)
    filled_blocks = int(bar_length * percentage / 100)
    
    # Create bar with different characters for animation effect
    bar_chars = ">"
    bar = ""
    for i in range(bar_length):
        if i < filled_blocks:
            # Use different characters for filled portion
            bar += Fore.GREEN + bar_chars[i % len(bar_chars)] + Style.RESET_ALL
        else:
            bar += Fore.BLUE + "░" + Style.RESET_ALL
    
    return f"[{bar}] {percentage}%"

def matrix_effect(width, lines=3):
    """Creates matrix-like falling characters effect"""
    chars = "--"
    effect = ""
    for _ in range(lines):
        line_length = min(50, width - 10)
        line = "".join(random.choice(chars) for _ in range(line_length))
        effect += Fore.GREEN + line + Style.RESET_ALL + "\n"
    return effect

def banner():
    """Displays the advanced hacker loading banner"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Get terminal width
    terminal_width = get_terminal_width()
    
    # Hacker colors
    COLOR_TITLE = Fore.GREEN + Style.BRIGHT
    COLOR_SUBTITLE = Fore.CYAN + Style.BRIGHT
    COLOR_EFFECT = Fore.BLUE + Style.BRIGHT
    COLOR_TEXT = Fore.WHITE + Style.BRIGHT
    COLOR_RESET = Style.RESET_ALL
    
    # Create dynamic frame
    frame_top, frame_side, frame_bottom = create_frame(terminal_width)
    
    # Loading states
    loading_states = [
        "🟢 INITIALIZING SYSTEM...",
        "🔵 LOADING CORE MODULES...",
        "🟣 STARTING ADVANCED TOOLS...", 
        "🟠 ACTIVATING SECURITY PROTOCOLS...",
        "🔴 VERIFYING SYSTEM INTEGRITY...",
        "🟢 ESTABLISHING CONNECTIONS...",
        "🔵 LOADING INTERFACE COMPONENTS...",
        "🟢 SYSTEM READY..."
    ]
    
    # Tool loading messages
    tool_messages = [
        "Loading encryption modules...",
        "Initializing network scanners...",
        "Starting penetration tools...",
        "Loading vulnerability database...",
        "Activating stealth mode...",
        "Configuring security protocols...",
        "Initializing data analysis...",
        "Loading advanced algorithms..."
    ]
    
    # Animation sequence
    print(COLOR_EFFECT + frame_top + COLOR_RESET)
    print(COLOR_EFFECT + frame_side + COLOR_RESET)
    
    for i in range(8):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Recalculate width in case terminal was resized
        current_width = get_terminal_width()
        frame_top, frame_side, frame_bottom = create_frame(current_width)
        
        print(COLOR_EFFECT + frame_top + COLOR_RESET)
        print(COLOR_EFFECT + frame_side + COLOR_RESET)
        
        # Main loading state
        state = loading_states[i]
        print(COLOR_EFFECT + frame_side[0] + COLOR_RESET + center_text(COLOR_TITLE + state + COLOR_RESET, current_width - 2) + COLOR_EFFECT + frame_side[-1] + COLOR_RESET)
        print(COLOR_EFFECT + frame_side + COLOR_RESET)
        
        # Progress bar
        progress = min(100, (i + 1) * 15)
        progress_bar = create_progress_bar(progress, current_width)
        print(COLOR_EFFECT + frame_side[0] + COLOR_RESET + center_text(progress_bar, current_width - 2) + COLOR_EFFECT + frame_side[-1] + COLOR_RESET)
        print(COLOR_EFFECT + frame_side + COLOR_RESET)
        
        # Tool loading message
        tool_message = tool_messages[i]
        print(COLOR_EFFECT + frame_side[0] + COLOR_RESET + center_text(COLOR_TEXT + tool_message + COLOR_RESET, current_width - 2) + COLOR_EFFECT + frame_side[-1] + COLOR_RESET)
        print(COLOR_EFFECT + frame_side + COLOR_RESET)
        
        # Matrix effect
        matrix = matrix_effect(current_width, 2)
        matrix_lines = matrix.strip().split('\n')
        for line in matrix_lines:
            print(COLOR_EFFECT + frame_side[0] + COLOR_RESET + center_text(line, current_width - 2) + COLOR_EFFECT + frame_side[-1] + COLOR_RESET)
        
        print(COLOR_EFFECT + frame_side + COLOR_RESET)
        print(COLOR_EFFECT + frame_bottom + COLOR_RESET)
        
        time.sleep(0.4)
    
    # Final banner
    time.sleep(0.4)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    final_width = get_terminal_width()
    frame_top, frame_side, frame_bottom = create_frame(final_width)
    
    print(COLOR_EFFECT + frame_top + COLOR_RESET)
    print(COLOR_EFFECT + frame_side + COLOR_RESET)
    
    # Final title
    final_title = "🚀 CREATOR: Brais Moure 🚀"
    print(COLOR_EFFECT + frame_side[0] + COLOR_RESET + center_text(COLOR_SUBTITLE + final_title + COLOR_RESET, final_width - 2) + COLOR_EFFECT + frame_side[-1] + COLOR_RESET)
    print(COLOR_EFFECT + frame_side + COLOR_RESET)
    
    # Success messages
    success_messages = [
        COLOR_TEXT + "✓ All systems initialized successfully",
        "✓ Advanced tools loaded and ready",
        "✓ Security protocols activated", 
        "✓ System running at optimal performance" + COLOR_RESET
    ]
    
    for message in success_messages:
        print(COLOR_EFFECT + frame_side[0] + COLOR_RESET + center_text(message, final_width - 2) + COLOR_EFFECT + frame_side[-1] + COLOR_RESET)
    
    print(COLOR_EFFECT + frame_side + COLOR_RESET)
    
    # Ready message
    ready_message = COLOR_TITLE + ">>> Dragon Black <<<" + COLOR_RESET
    print(COLOR_EFFECT + frame_side[0] + COLOR_RESET + center_text(ready_message, final_width - 2) + COLOR_EFFECT + frame_side[-1] + COLOR_RESET)
    
    print(COLOR_EFFECT + frame_side + COLOR_RESET)
    print(COLOR_EFFECT + frame_bottom + COLOR_RESET)

# Installation and usage:
# pip install colorama

