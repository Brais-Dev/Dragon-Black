#!/usr/bin/env python3
"""
Script de utilidad para crear nuevos plugins de Dragon-Black
"""

import os
import json
import sys
from pathlib import Path

def create_plugin():
    print("=== Dragon-Black Plugin Creation Assistant ===\n")

    # Pedir información del plugin
    name = input("Plugin name (no spaces, use hyphens or underscores): ").strip()
    if not name:
        print("Plugin name is required.")
        return

    version = input("Plugin version [1.0.0]: ").strip() or "1.0.0"
    author = input("Plugin author: ").strip()
    if not author:
        print("Plugin author is required.")
        return

    description = input("Plugin description: ").strip()
    if not description:
        print("Plugin description is required.")
        return

    command = input(f"Main command for the plugin [{name}]: ").strip() or name

    # Crear directorio del plugin
    plugin_dir = Path(name)
    if plugin_dir.exists():
        print(f"Directory {name} already exists. Please choose another name or remove the existing directory.")
        return

    plugin_dir.mkdir()

    # Crear manifest.json
    manifest = {
        "name": name,
        "version": version,
        "author": author,
        "description": description,
        "source": f"https://github.com/{author.lower()}/{name}.git",
        "git_url": f"https://github.com/{author.lower()}/{name}.git",
        "main": "plugin.py",
        "command": command,
        "default_function": "main"
    }

    with open(plugin_dir / "manifest.json", 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Crear plugin.py con plantilla
    plugin_content = f'''# Plugin: {name}
# Author: {author}
# Description: {description}
"""
libraries required
"""
from typing import Dict, Callable
import os

def main_function():
    """
    Main function of your plugin
    """
    print("Hello from {name}!")
    # Place your plugin logic here


"""
Main function that runs when the plugin command is called
"""
def main():
    main_function()

"""
Function that runs when the plugin is loaded
"""
def install():
    print("{name} loaded successfully")


"""
This function shows a message when a plugin is removed or uninstalled
"""
def uninstall():    
    print("{name} was uninstalled correctly")

"""
This function shows a message when a plugin is removed or uninstalled
"""
def uninstall():
    print("{name} was uninstalled correctly")

"""
Function that registers additional plugin commands
"""
def register_commands() -> Dict[str, Callable]:
    return {{
        "{command}": main_function
    }}
'''

    with open(plugin_dir / "plugin.py", 'w', encoding='utf-8') as f:
        f.write(plugin_content)

    print(f"\nPlugin '{name}' created successfully!")
    print(f"Directory: {plugin_dir.absolute()}")
    print(f"\nNext steps:")
    print(f"1. Review and modify files in {plugin_dir}/")
    print(f"2. Test your plugin with: dragon")
    print(f"3. Install your plugin with: plugin install {plugin_dir.absolute()}")
    print(f"4. To distribute, upload your plugin to a Git repository")

if __name__ == "__main__":
    create_plugin()
