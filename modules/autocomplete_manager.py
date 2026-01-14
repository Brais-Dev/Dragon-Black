# modules/autocomplete_manager.py
"""
Autocomplete manager with easy configuration
Handles command completion with customizable colors and categories
"""

import os
import stat
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.formatted_text import HTML
from modules.color_config import ColorTheme

class PathCompleter(Completer):
    """Custom completer that handles both commands and file paths"""

    def __init__(self, commands):
        self.commands = commands
        self.command_set = set(commands)  # For faster lookup

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()

        # If there are no words or just one incomplete word, suggest commands
        if len(words) == 0 or (len(words) == 1 and text.endswith(words[0])):
            # Provide command completions
            for cmd in self.commands:
                if cmd.lower().startswith(text.lower()):
                    yield Completion(cmd, start_position=-len(text))
        else:
            # More than one word, check if first word is a command that takes paths
            first_word = words[0].lower()
            if first_word in ['cd', 'ls', 'cat', 'less', 'more', 'nano', 'vim', 'vi', 'cp', 'mv', 'rm', 'mkdir', 'rmdir', 'pwd', 'head', 'tail', 'grep', 'find']:
                # This command likely takes a file/directory path
                path_prefix = words[-1]  # Last word is what we're completing

                # Determine the directory to search in
                if path_prefix.startswith('/'):
                    # Absolute path
                    search_dir = os.path.dirname(path_prefix) or '/'
                    prefix_base = os.path.basename(path_prefix)
                elif path_prefix.startswith('~/'):
                    # Home-relative path
                    expanded_home = os.path.expanduser('~')
                    rel_path = path_prefix[2:]  # Remove ~/
                    search_dir = os.path.dirname(os.path.join(expanded_home, rel_path)) or expanded_home
                    prefix_base = os.path.basename(rel_path)
                else:
                    # Relative path
                    search_dir = os.path.dirname(path_prefix) or '.'
                    prefix_base = os.path.basename(path_prefix)

                # Expand ~ if present
                if path_prefix.startswith('~/'):
                    search_dir = os.path.expanduser(search_dir)

                try:
                    # List contents of the directory
                    if os.path.isdir(search_dir):
                        for item in os.listdir(search_dir):
                            if item.lower().startswith(prefix_base.lower()):
                                item_path = os.path.join(search_dir, item)

                                # Add trailing slash for directories
                                if os.path.isdir(item_path):
                                    completion_text = item + '/'
                                else:
                                    completion_text = item

                                # Calculate the text to append
                                if path_prefix:
                                    start_pos = -len(path_prefix)
                                else:
                                    start_pos = 0

                                yield Completion(completion_text, start_position=start_pos)
                except:
                    # If we can't read the directory, just return command completions
                    pass


class AutoCompleteManager:
    """Manages autocomplete with easy configuration"""

    def __init__(self, commands_list, theme="default"):
        """
        Initialize the autocomplete manager

        Args:
            commands_list: List of commands for autocomplete
            theme: Name of the color theme to use
        """
        self.commands = commands_list
        self.theme_name = theme
        self.theme = ColorTheme.get_theme(theme)
        self.completer = self._create_completer()
        
    def _create_completer(self):
        """Create completer based on command list"""
        return PathCompleter(self.commands)
    
    def get_style(self):
        """
        Get the configured style
        
        Returns:
            Style object for prompt_toolkit
        """
        return self.theme
    
    def get_completer(self):
        """
        Get the autocomplete object
        
        Returns:
            Completer object
        """
        return self.completer
    
    def set_theme(self, theme_name):
        """
        Change color theme
        
        Args:
            theme_name: Name of the theme to use
            
        Returns:
            self for method chaining
        """
        self.theme_name = theme_name
        self.theme = ColorTheme.get_theme(theme_name)
        return self
    
    def get_current_theme(self):
        """
        Get current theme name
        
        Returns:
            Current theme name as string
        """
        return self.theme_name
    
    def add_commands(self, new_commands):
        """
        Add new commands to autocomplete

        Args:
            new_commands: List of new commands to add

        Returns:
            self for method chaining
        """
        # Avoid duplicates
        for cmd in new_commands:
            if cmd not in self.commands:
                self.commands.append(cmd)

        # Update the command set for faster lookup
        self.completer = self._create_completer()
        return self
    
    def remove_command(self, command):
        """
        Remove a command from autocomplete
        
        Args:
            command: Command to remove
            
        Returns:
            self for method chaining
        """
        if command in self.commands:
            self.commands.remove(command)
            self.completer = self._create_completer()
        return self
    
    def clear_commands(self):
        """
        Clear all commands from autocomplete
        
        Returns:
            self for method chaining
        """
        self.commands = []
        self.completer = self._create_completer()
        return self
    
    def get_commands(self):
        """
        Get list of all commands
        
        Returns:
            List of commands
        """
        return self.commands.copy()
    
    def create_categorized_completer(self, categories_dict):
        """
        Create a completer with categorized commands
        
        Args:
            categories_dict: Dictionary with {category: [commands]}
            
        Returns:
            Custom Completer object
        """
        class CategorizedCompleter(Completer):
            def get_completions(self, document, complete_event):
                text = document.text_before_cursor.lower()
                
                for category, commands in categories_dict.items():
                    for cmd in commands:
                        if cmd.startswith(text):
                            # Color based on category
                            category_colors = {
                                'system': '#ff5555',    # Red for system
                                'network': '#55ff55',   # Green for network
                                'tools': '#5555ff',     # Blue for tools
                                'dragon': '#ff55ff',    # Purple for dragon
                                'install': '#ffff55',   # Yellow for install
                                'file': '#55ffff',      # Cyan for file
                            }
                            
                            color = category_colors.get(category, '#ffffff')
                            
                            yield Completion(
                                cmd,
                                start_position=-len(text),
                                display=HTML(
                                    f'<style fg="{color}">'
                                    f'{cmd}'
                                    f'<style fg="#888888"> ({category})</style>'
                                    f'</style>'
                                )
                            )
        
        return CategorizedCompleter()
    
    def update_from_categories(self, categories_dict):
        """
        Update commands from categories dictionary
        
        Args:
            categories_dict: Dictionary with {category: [commands]}
            
        Returns:
            self for method chaining
        """
        all_commands = []
        for commands in categories_dict.values():
            all_commands.extend(commands)
        
        self.commands = list(set(all_commands))  # Remove duplicates
        self.completer = self._create_completer()
        return self
    
    def search_commands(self, keyword):
        """
        Search commands containing keyword
        
        Args:
            keyword: String to search for
            
        Returns:
            List of matching commands
        """
        return [cmd for cmd in self.commands if keyword.lower() in cmd.lower()]
    
    def get_external_commands(self):
        """
        Get list of external commands from Termux directories

        Returns:
            List of external command names
        """
        external_commands = []

        # Common Termux command directories
        command_dirs = [
            os.path.join(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"), "bin"),
            os.path.join(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"), "bin", "applets"),
        ]

        for cmd_dir in command_dirs:
            if os.path.exists(cmd_dir):
                try:
                    for item in os.listdir(cmd_dir):
                        item_path = os.path.join(cmd_dir, item)

                        # Check if it's a file and executable
                        if os.path.isfile(item_path) and os.access(item_path, os.X_OK):
                            # Avoid duplicates
                            if item not in external_commands and item not in self.commands:
                                external_commands.append(item)
                except PermissionError:
                    # Skip if we don't have permission to read the directory
                    continue

        return external_commands

    def refresh_commands(self):
        """
        Refresh the command list with both internal and external commands

        Returns:
            self for method chaining
        """
        # Get external commands
        external_commands = self.get_external_commands()

        # Combine internal and external commands
        all_commands = list(set(self.commands + external_commands))

        # Update the commands list
        self.commands = all_commands

        # Recreate the completer
        self.completer = self._create_completer()

        return self

    def command_count(self):
        """
        Get total number of commands

        Returns:
            Integer count of commands
        """
        return len(self.commands)