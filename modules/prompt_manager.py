# modules/prompt_manager.py
"""
Prompt manager with centralized configuration
Handles user input with autocomplete and themes
"""

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory, FileHistory
from modules.autocomplete_manager import AutoCompleteManager

class DragonPromptManager:
    """Main prompt manager for Dragon system"""
    
    def __init__(self, commands_list, theme="default", use_history=True):
        """
        Initialize prompt manager
        
        Args:
            commands_list: List of commands for autocomplete
            theme: Color theme name
            use_history: Whether to enable command history
        """
        self.ac_manager = AutoCompleteManager(commands_list, theme)
        self.history = self._create_history() if use_history else None
        self.session = self._create_session()
        self.prompt_count = 0
        
    def _create_history(self):
        """Create command history storage"""
        try:
            # Try to use file history, fallback to memory
            return FileHistory('.dragon_history')
        except:
            return InMemoryHistory()
    
    def _create_session(self):
        """Create prompt session with configuration"""
        return PromptSession(
            completer=self.ac_manager.get_completer(),
            complete_while_typing=True,
            style=self.ac_manager.get_style(),
            complete_style='multi_column',
            reserve_space_for_menu=8,
            history=self.history,
            enable_history_search=True,
            search_ignore_case=True,
        )
    
    def get_prompt(self, message="dragon@>>> "):
        """
        Get user input with autocomplete
        
        Args:
            message: Prompt message to display
            
        Returns:
            Command entered by user
        """
        self.prompt_count += 1
        
        # Create colored prompt
        prompt_html = HTML(f'<style fg="green">{message}</style>')
        
        try:
            user_input = self.session.prompt(prompt_html)
            return user_input.strip()
        except KeyboardInterrupt:
            return ""
        except EOFError:
            return "exit"
    
    def change_theme(self, theme_name):
        """
        Change color theme
        
        Args:
            theme_name: Name of theme to use
            
        Returns:
            self for method chaining
        """
        self.ac_manager.set_theme(theme_name)
        self.session = self._create_session()
        return self
    
    def add_commands(self, new_commands):
        """
        Add new commands to autocomplete
        
        Args:
            new_commands: List of new commands
            
        Returns:
            self for method chaining
        """
        self.ac_manager.add_commands(new_commands)
        self.session = self._create_session()
        return self
    
    def get_theme_info(self):
        """
        Get information about current theme
        
        Returns:
            Dictionary with theme information
        """
        from modules.color_config import ColorTheme
        return ColorTheme.get_theme_info(self.ac_manager.get_current_theme())
    
    def list_themes(self):
        """
        List all available themes
        
        Returns:
            List of theme names
        """
        from modules.color_config import ColorTheme
        return ColorTheme.list_themes()
    
    def show_theme_info(self):
        """Display current theme information"""
        theme_info = self.get_theme_info()
        print(f"\nCurrent Theme: {theme_info['name']}")
        print(f"Description: {theme_info['description']}")
        print(f"Available themes: {', '.join(self.list_themes())}")
        return self
    
    def reset_history(self):
        """Reset command history"""
        self.history = self._create_history()
        self.session = self._create_session()
        return self
    
    def get_history_count(self):
        """
        Get number of commands in history
        
        Returns:
            Number of history entries or 0 if disabled
        """
        if self.history and hasattr(self.history, 'load_history_strings'):
            try:
                return len(list(self.history.load_history_strings()))
            except:
                return 0
        return 0
    
    def clear_history(self):
        """Clear command history"""
        if self.history:
            if hasattr(self.history, 'clear'):
                self.history.clear()
            self.history = self._create_history()
            self.session = self._create_session()
        return self
    
    def get_stats(self):
        """
        Get usage statistics
        
        Returns:
            Dictionary with statistics
        """
        return {
            'prompt_count': self.prompt_count,
            'command_count': self.ac_manager.command_count(),
            'theme': self.ac_manager.get_current_theme(),
            'history_entries': self.get_history_count(),
        }
    
    def create_custom_prompt(self, **kwargs):
        """
        Create custom prompt with additional options
        
        Args:
            **kwargs: Additional prompt options
            
        Returns:
            Custom PromptSession
        """
        default_options = {
            'completer': self.ac_manager.get_completer(),
            'complete_while_typing': True,
            'style': self.ac_manager.get_style(),
            'complete_style': 'multi_column',
            'reserve_space_for_menu': 8,
            'history': self.history,
        }
        
        # Update defaults with provided options
        default_options.update(kwargs)
        
        return PromptSession(**default_options)
    
    def prompt_with_message(self, message, default=""):
        """
        Prompt with specific message and optional default
        
        Args:
            message: Prompt message
            default: Default value
            
        Returns:
            User input or default
        """
        prompt_html = HTML(f'<style fg="cyan">{message}</style>')
        
        try:
            user_input = self.session.prompt(
                prompt_html,
                default=default
            )
            return user_input.strip()
        except KeyboardInterrupt:
            return default
        except EOFError:
            return default