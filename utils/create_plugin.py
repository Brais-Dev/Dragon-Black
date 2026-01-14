#!/usr/bin/env python3
"""
Scrip
"""

import os
import json
import sys
from pathlib import Path

real_path = os.path.realpath(__file__)
project_root = os.path.abspath(os.path.join(os.path.dirname(real_path), '..'))
sys.path.insert(0, project_root)
# Importar el sistema de traducción
from core.configuration_language import Translator
app = Translator()
 

def create_plugin():
    print(f"{app.t('plugin_creation_assistant')}\n")

    # Pedir información del plugin
    name = input(app.t("plugin_name_prompt")).strip()
    if not name:
        print(app.t("plugin_name_required"))
        return

    version = input(app.t("plugin_version_prompt")).strip() or "1.0.0"
    author = input(app.t("plugin_author_prompt")).strip()
    if not author:
        print(app.t("plugin_author_required"))
        return

    description = input(app.t("plugin_description_prompt")).strip()
    if not description:
        print(app.t("plugin_description_required"))
        return

    command = input(app.t("plugin_command_prompt").format(name=name)).strip() or name

    # Crear directorio del plugin
    plugin_dir = Path(name)
    if plugin_dir.exists():
        print(app.t("directory_exists").format(name=name))
        return

    plugin_dir.mkdir()

    # Preguntar por dependencias
    requirements_input = input(app.t("plugin_requirements_prompt")).strip()
    requirements = []
    if requirements_input:
        requirements = [req.strip() for req in requirements_input.split(',') if req.strip()]

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

    # Agregar requirements solo si hay alguno
    if requirements:
        manifest["requirements"] = requirements

    with open(plugin_dir / "manifest.json", 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Crear plugin.py con plantilla
    plugin_content = f'''# Plugin: {name}
# Author: {author}
# Description: {description}
"""
Requirements: {", ".join(requirements) if requirements else "None"}
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
Function that registers additional plugin commands
"""
def register_commands() -> Dict[str, Callable]:
    return {{
        "{command}": main_function
    }}
'''

    with open(plugin_dir / "plugin.py", 'w', encoding='utf-8') as f:
        f.write(plugin_content)

    print(f"\n{app.t('plugin_created_success').format(name=name)}")
    print(f"{app.t('plugin_directory').format(path=plugin_dir.absolute())}")
    print(f"\n{app.t('next_steps')}")
    print(f"{app.t('review_files').format(path=plugin_dir)}")
    print(f"{app.t('test_plugin')}")
    print(f"{app.t('install_plugin').format(path=plugin_dir.absolute())}")
    print(f"{app.t('distribute_plugin')}")

if __name__ == "__main__":
    create_plugin()
