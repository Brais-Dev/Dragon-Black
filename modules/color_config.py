# modules/color_config.py
"""
Color configuration module for Dragon's autocomplete
Easy color theme management for prompt_toolkit
"""

from prompt_toolkit.styles import Style

class ColorTheme:
    """Class to manage autocomplete color themes"""
    
    @staticmethod
    def dragon_default():
        """Default Dragon theme (green and black) - Hacker style"""
        return Style.from_dict({
            # Main prompt
            'prompt': '#00ff00 bold',
            
            # User input text
            'input': '#ffff00',
            
            # Autocomplete menu
            'completion-menu': 'bg:#000000',
            'completion-menu.border': '#00ffff',
            
            # Menu items
            'completion-menu.completion': 'bg:#003333 #00ffff',
            'completion-menu.completion.current': 'bg:#00ffff #000000 bold',
            
            # Scrollbar
            'scrollbar.background': 'bg:#002222',
            'scrollbar.button': 'bg:#00aaaa',
            
            # Selection highlight
            'selected': 'bg:#00ffff #000000',
        })
    
    @staticmethod
    def dark_green():
        """Dark green theme - Easy on the eyes"""
        return Style.from_dict({
            'prompt': '#00aa00 bold',
            'input': '#aaffaa',
            'completion-menu': 'bg:#001100',
            'completion-menu.border': '#00ff00',
            'completion-menu.completion': 'bg:#003300 #88ff88',
            'completion-menu.completion.current': 'bg:#00aa00 #001100 bold',
            'scrollbar.background': 'bg:#002200',
            'scrollbar.button': 'bg:#00aa00',
        })
    
    @staticmethod
    def blue_terminal():
        """Blue terminal theme - Classic look"""
        return Style.from_dict({
            'prompt': '#0088ff bold',
            'input': '#aaccff',
            'completion-menu': 'bg:#000033',
            'completion-menu.border': '#0088ff',
            'completion-menu.completion': 'bg:#001133 #88bbff',
            'completion-menu.completion.current': 'bg:#0088ff #000033 bold',
            'scrollbar.background': 'bg:#001122',
            'scrollbar.button': 'bg:#0088ff',
        })
    
    @staticmethod
    def red_alert():
        """Red alert theme - For warnings and critical systems"""
        return Style.from_dict({
            'prompt': '#ff0000 bold',
            'input': '#ff8888',
            'completion-menu': 'bg:#330000',
            'completion-menu.border': '#ff0000',
            'completion-menu.completion': 'bg:#550000 #ffaaaa',
            'completion-menu.completion.current': 'bg:#ff0000 #330000 bold',
            'scrollbar.background': 'bg:#220000',
            'scrollbar.button': 'bg:#ff0000',
        })
    
    @staticmethod
    def purple_hacker():
        """Purple hacker theme - Modern and stylish"""
        return Style.from_dict({
            'prompt': '#aa00ff bold',
            'input': '#cc88ff',
            'completion-menu': 'bg:#110022',
            'completion-menu.border': '#aa00ff',
            'completion-menu.completion': 'bg:#220044 #bb88ff',
            'completion-menu.completion.current': 'bg:#aa00ff #110022 bold',
            'scrollbar.background': 'bg:#170017',
            'scrollbar.button': 'bg:#aa00ff',
        })
    
    @staticmethod
    def matrix():
        """Matrix theme - Green on black, classic hacker"""
        return Style.from_dict({
            'prompt': '#00ff00 bold',
            'input': '#00ff00',
            'completion-menu': 'bg:#001100',
            'completion-menu.border': '#00ff00',
            'completion-menu.completion': 'bg:#002200 #00ff00',
            'completion-menu.completion.current': 'bg:#00ff00 #001100',
            'scrollbar.background': 'bg:#001100',
            'scrollbar.button': 'bg:#00ff00',
        })
    
    @staticmethod
    def solarized_dark():
        """Solarized dark theme - Professional and popular"""
        return Style.from_dict({
            'prompt': '#2aa198 bold',  # Cyan
            'input': '#93a1a1',        # Base0
            'completion-menu': 'bg:#002b36',  # Base03
            'completion-menu.border': '#586e75',  # Base01
            'completion-menu.completion': 'bg:#073642 #839496',  # Base02, Base1
            'completion-menu.completion.current': 'bg:#268bd2 #fdf6e3',  # Blue, Base3
            'scrollbar.background': 'bg:#073642',
            'scrollbar.button': 'bg:#268bd2',
        })
    
    @staticmethod
    def get_theme(theme_name="dragon_default"):
        """
        Get a theme by name
        
        Args:
            theme_name: Name of the theme to retrieve
            
        Returns:
            Style object for the requested theme
        """
        themes = {
            "default": ColorTheme.dragon_default,
            "dragon": ColorTheme.dragon_default,
            "dark_green": ColorTheme.dark_green,
            "blue": ColorTheme.blue_terminal,
            "red": ColorTheme.red_alert,
            "purple": ColorTheme.purple_hacker,
            "matrix": ColorTheme.matrix,
            "solarized": ColorTheme.solarized_dark,
        }
        
        # Get theme function or use default
        theme_func = themes.get(theme_name.lower(), ColorTheme.dragon_default)
        return theme_func()
    
    @staticmethod
    def list_themes():
        """List all available theme names"""
        return [
            "default",
            "dragon",
            "dark_green", 
            "blue",
            "red",
            "purple",
            "matrix",
            "solarized"
        ]
    
    @staticmethod
    def get_theme_info(theme_name):
        """
        Get information about a specific theme
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            Dictionary with theme information
        """
        theme_descriptions = {
            "default": "Default Dragon theme - Green hacker style",
            "dragon": "Default Dragon theme - Green hacker style",
            "dark_green": "Dark green theme - Easy on eyes",
            "blue": "Blue terminal - Classic look",
            "red": "Red alert - For warnings",
            "purple": "Purple hacker - Modern style",
            "matrix": "Matrix style - Green on black",
            "solarized": "Solarized dark - Professional theme",
        }
        
        return {
            "name": theme_name,
            "description": theme_descriptions.get(theme_name, "Unknown theme"),
            "available": theme_name in ColorTheme.list_themes()
        }