"""
Input validation module for Dragon-Black
Provides security validation for user inputs to prevent malicious commands
"""
import re
from typing import Union, List, Tuple
from core.configuration_language import app


class InputValidator:
    """Validates user inputs to prevent security issues"""

    def __init__(self):
        # Define dangerous patterns that should be blocked
        self.dangerous_patterns = [
          r'•']
       
        # Define valid command patterns (whitelist approach)
        self.valid_command_pattern = re.compile(
            r'^[a-zA-Z0-9_\- \./]+$'  # Allow alphanumeric, spaces, hyphens, underscores, dots, slashes
        )

        # Specific allowed commands (for commands that might include special chars)
        self.allowed_patterns = [
            r'^drg install [a-zA-Z0-9_\-]+$',  # Install command
            r'^drg uninstall [a-zA-Z0-9_\-]+$',  # Uninstall command
            r'^drg search [a-zA-Z0-9_\- ]+$',  # Search command
            r'^drg info [a-zA-Z0-9_\-]+$',  # Info command
            r'^theme set [a-zA-Z0-9_\-]+$',  # Theme command
            r'^tools$',  # Tools command
            r'^languages$',  # Languages command
            r'^exit$',  # Exit command
        ]

        self.allowed_pattern_compiled = [re.compile(pattern) for pattern in self.allowed_patterns]

    def is_command_safe(self, cmd: str) -> Tuple[bool, str]:
        """
        Check if a command is safe to execute

        Args:
            cmd: Command string to validate

        Returns:
            Tuple of (is_safe, reason)
        """
        if not cmd or not isinstance(cmd, str):
            return False, app.get_error_message("invalid_command")

        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, cmd):
                return False, app.get_error_message("command_rejected", f"Dangerous pattern detected: {pattern}")

        # Check against allowed patterns
        for pattern in self.allowed_pattern_compiled:
            if pattern.match(cmd):
                return True, "Matched allowed pattern"

        # For commands that don't match allowed patterns, use general validation
        if self.valid_command_pattern.match(cmd.strip()):
            return True, "Valid command pattern"

        return False, app.get_error_message("invalid_command")

    def sanitize_command(self, cmd: str) -> str:
        """
        Sanitize a command by removing potentially harmful characters
        Note: This is a secondary defense, validation should be primary
        """
        # Remove potential command separators (but keep spaces for arguments)
        sanitized = re.sub(r'[;&|`$]', '', cmd)
        # Limit length to prevent buffer overflow attempts
        return sanitized[:1000]  # Limit to 1000 characters

    def validate_package_name(self, package_name: str) -> Tuple[bool, str]:
        """
        Validate a package name specifically

        Args:
            package_name: Name of the package to validate

        Returns:
            Tuple of (is_valid, reason)
        """
        if not package_name:
            return False, app.get_error_message("invalid_command")

        # Check for invalid characters in package name
        if re.search(r'[;&|`$<>{}[\]~#^*+=?%]', package_name):
            return False, "Package name contains invalid characters"

        # Check length
        if len(package_name) > 100:
            return False, "Package name too long"

        # Check format (only alphanumeric, hyphens, underscores)
        if not re.match(r'^[a-zA-Z0-9_\-]+$', package_name):
            return False, "Package name contains invalid characters"

        return True, "Valid package name"

    def validate_theme_name(self, theme_name: str) -> Tuple[bool, str]:
        """
        Validate a theme name specifically

        Args:
            theme_name: Name of the theme to validate

        Returns:
            Tuple of (is_valid, reason)
        """
        if not theme_name:
            return False, "Empty theme name"

        # Check format (only alphanumeric, hyphens, underscores)
        if not re.match(r'^[a-zA-Z0-9_\-]+$', theme_name):
            return False, "Theme name contains invalid characters"

        return True, "Valid theme name"

    def validate_file_path(self, path: str) -> Tuple[bool, str]:
        """
        Validate a file path to prevent directory traversal

        Args:
            path: File path to validate

        Returns:
            Tuple of (is_valid, reason)
        """
        if not path:
            return False, "Empty path"

        # Check for directory traversal attempts
        if '..' in path or './' in path or '../' in path:
            return False, "Path contains directory traversal"

        # Check for potentially malicious characters
        if re.search(r'[;&|`$<>{}~#^*+=?%]', path):
            return False, "Path contains invalid characters"

        return True, "Valid file path"


# Global validator instance
validator = InputValidator()


def validate_command(cmd: str) -> Tuple[bool, str]:
    """
    Convenience function to validate a command

    Args:
        cmd: Command to validate

    Returns:
        Tuple of (is_safe, reason)
    """
    return validator.is_command_safe(cmd)


def sanitize_input(user_input: str) -> str:
    """
    Convenience function to sanitize user input

    Args:
        user_input: Raw user input

    Returns:
        Sanitized input
    """
    return validator.sanitize_command(user_input)


def validate_package_name(package_name: str) -> Tuple[bool, str]:
    """
    Convenience function to validate package name

    Args:
        package_name: Name of package to validate

    Returns:
        Tuple of (is_valid, reason)
    """
    return validator.validate_package_name(package_name)


def validate_theme_name(theme_name: str) -> Tuple[bool, str]:
    """
    Convenience function to validate theme name

    Args:
        theme_name: Name of theme to validate

    Returns:
        Tuple of (is_valid, reason)
    """
    return validator.validate_theme_name(theme_name)


def validate_file_path(path: str) -> Tuple[bool, str]:
    """
    Convenience function to validate file path

    Args:
        path: Path to validate

    Returns:
        Tuple of (is_valid, reason)
    """
    return validator.validate_file_path(path)