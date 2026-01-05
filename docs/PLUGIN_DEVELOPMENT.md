# Plugin Development Guide for Dragon-Black CLI

[![Version](https://img.shields.io/badge/version-1.0.3-blue.svg)](https://github.com/Brais-Dev/Dragon-Black)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Termux-green.svg)](https://termux.com/)
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)](https://github.com/Brais-Dev/Dragon-Black)
[![Development](https://img.shields.io/badge/development-supported-success.svg)](../README.md)
[![Development](https://img.shields.io/badge/development-supported-success.svg)](../README.md)


## Introduction

Plugin installation in Dragon-Black CLI is a simple process that allows extending the system's functionalities with tools developed by the community. This guide provides detailed and professional instructions for installing, managing, and maintaining plugins in Dragon-Black CLI.

---

## Plugin Development Introduction

The Dragon-Black CLI plugin system is a modular architecture that allows extending the main system's functionalities. This feature allows developers and community members to create custom tools that integrate perfectly with the Dragon-Black CLI interface.

### Plugin System Objectives

- **Extensibility**: Allow adding new functionalities without modifying the core
- **Community**: Facilitate community contribution with custom tools
- **Modularity**: Keep the main system clean and organized
- **Security**: Provide a secure environment for executing external code
- **Integration**: Ensure plugins integrate perfectly with the system

---

## Plugin Structure

### Basic Structure

Plugin structure:

```
plugin_name/
├── plugin.py          # Main plugin file
├── manifest.json      # Plugin metadata
├── README.md          # Plugin documentation
├── LICENSE            # Plugin license
```

### Component Description

#### plugin.py
Main file containing the plugin logic.

#### manifest.json
File containing essential plugin metadata, such as name, version, author, etc.

#### README.md
Plugin documentation explaining its functionality and usage.

#### LICENSE
License file defining the plugin usage terms.

---
## Manifest File

### Manifest Structure

The `manifest.json` file contains certain information about the plugin and must contain:

```json
{
  "name": "plugin_name",
  "version": "1.0.0",
  "author": "Author Name",
  "description": "brief and clear description",
  "main": "plugin.py",
  "source": "https://github.com/user/plugin_name",
  "git_url": "https://github.com/user/plugin_name",
  "command": "command_name that executes the plugin",
  "default_function": "main"
}
```

### Required Fields

#### name (string)
Unique name of the plugin

#### version
Plugin version in semver format (X.Y.Z). Example: "1.0.0"

#### author (string)
Name of the plugin author.

#### description (string)
Clear and concise description of the plugin functionality.

#### main (string)
Name of the main plugin file (usually "plugin.py"), other names are not valid!

#### command (string)
Main command that invokes the plugin.

### source
Git repository URL of the plugin.

#### git_url (string)
Git repository URL of the plugin. (same as source)

#### default_function (string)
Name of the default function to execute
default main.

---

## Main Plugin File

### Basic Structure

The `plugin.py` file must contain:

```python

"""
these libraries are imported only as an example, they are not required
"""
from typing import Dict, Callable
"""

this is the function of our tool
"""
def my_tool():
    """
    implement the logic of our tool here
    """
    print("Hello from my tool!")


"""
this function handles calling our tool's function
"""
def main():
    # here the function is called
    my_tool()

"""
this function displays a message when a plugin is loaded and installed
"""
def install():
    print("hydra loaded successfully")

"""
this function handles displaying a message when the plugin is uninstalled
"""
def uninstall():
    print("hydra uninstalled correctly ")

def main_function():
    print("Main function of the plugin")

def register_commands() -> Dict[str, Callable]:
    return {
        "hydra": main_function
    }


```

### Required Functions

#### main()
Main function that executes when the plugin command is invoked. It is mandatory in all plugins.

### Optional Functions

#### register_commands()
Returns a dictionary with additional commands that the plugin can register.

#### install()
Executes during plugin installation. Useful for installing dependencies.

#### uninstall()
Executes during plugin uninstallation. Useful for cleaning up resources.

The functions **install()**, **uninstall()**, **register_commands()** are optional and not mandatory
**Note** both files must be named `plugin.py` and `manifest.json`

### Create plugin easily
You can easily create a plugin using a tool that Dragon-Black includes.
The plugin creation tool that Dragon-Black includes helps you fill out the **manifest.json** file and the **plugin.py** file

### how it works
the plugin creation tool
requests the data that manifest.json requires to create the plugin and reloads the **manifest.json**

### how to use
- 1 inside the termux shell execute the following command

```dragon
dragon --create-plugin
```
this will open the plugin creation tool

## manual method
to create your plugin manually
- 1 create your plugin directory
- 2 create the plugin.py file
- 3 create the manifest.json file with the required data

**Note:**
the automatic method saves you a lot of time


## Local Testing of a plugin
Dragon-Black allows you to test your plugin locally, this is necessary when you are developing the plugin because you need to do tests to ensure the plugin works correctly
to install your plugin locally
you just need to pass the plugin path to Dragon-Black

```dragon
dragon install <plugin_path>
```
the plugin will be installed locally

## Plugin Distribution
to distribute your plugin in the official Dragon-Black plugin manager repository you must meet the following requirements

- **1 verify functionality:** test the plugin locally
- **2 verify files** verify that manifest.json contains all the data
- **3 verify names** verify that the files have the names manifest.json, and plugin.py

once you have everything in order go to the official plugin manager repo

[Dragon-Black-Plugins](https://github.com/Brais-Dev/Dragon-Black-Plugins)

once you are in the official repo

- **1 fork the repo:** github will give you an exact copy of the repo
- **2 clone the copy that github gave you to the Termux shell**
- **3 Create a public repo for your plugin**
- **4 upload your plugin to the repo you created**
- **5 now move the folder where your plugin is to Dragon-Black-Plugins**
- **5 make a pull request**