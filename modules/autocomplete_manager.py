# modules/autocomplete_manager.py
"""
Autocomplete manager with easy configuration
Handles command completion with customizable colors and categories
"""

from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.formatted_text import HTML
from modules.color_config import ColorTheme

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
        return WordCompleter(self.commands, ignore_case=True)
    
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
    
    def command_count(self):
        """
        Get total number of commands
        
        Returns:
            Integer count of commands
        """
        return len(self.commands)