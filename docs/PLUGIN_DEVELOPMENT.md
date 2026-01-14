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

## Introduction to Plugin Development

The Dragon-Black CLI plugin system is a modular architecture that allows extending the main system's functionalities. This feature allows developers and community members to create custom tools that integrate perfectly with the Dragon-Black CLI interface.

### Plugin System Objectives

- **Extensibility**: Allow adding new functionalities without modifying the core
- **Community**: Facilitate community contribution with custom tools
- **Modularity**: Keep the main system clean and organized
- **Security**: Provide a secure environment for running external code
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
Main file that contains the plugin logic.

#### manifest.json
File that contains essential plugin metadata, such as name, version, author, etc.

#### README.md
Plugin documentation explaining its functionality and usage.

#### LICENSE
License file that defines the terms of use of the plugin.

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
  "default_function": "main",
  "requirements": ["list", "of", "dependencies"]
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
URL of the plugin Git repository.

#### git_url (string)
URL of the plugin Git repository. (same as source)

#### default_function (string)
Name of the default function to execute
default main.

#### requirements (array, optional)
List of Python dependencies required by the plugin the `requirements` field should only contain dependencies that the plugin may need, separated by commas example
``["rich","colorama","prompt_toolkit"]`` the Dragon-Black system takes care of verifying that they are Python libraries and installs them if the plugin does not require dependencies the `requirements` field can be optional

---

## Main Plugin File

### Basic Structure

The `plugin.py` file must contain:

```python

"""
these libraries are imported only as an example, they are not mandatory
"""
from typing import Dict, Callable
"""

this is the function of our tool
"""
def my_function():
    """
    here the logic of our tool is implemented
    """
    print("Hello from my tool!")


"""
this function handles the call to our tool function (Required)
"""
def main():
    # here the function is called
    my_function()

"""
this function displays a message when a plugin is loaded and installed (optional)
"""
def install():
    print("hydra loaded successfully")

"""
this function displays a message when the plugin is uninstalled (optional)
"""
def uninstall():
    print("hydra uninstalled correctly ")

"""
this function creates a dictionary with the command and the function (optional)
"""
def register_commands() -> Dict[str, Callable]:
    return {
        "hydra": main_function
    }


```

### Required Functions

#### main()
Main function that runs when the plugin command is invoked. It is mandatory in all plugins.

### Optional Functions

#### register_commands()
Returns a dictionary with additional commands with which the plugin can be executed, it is optional

#### install()
Runs during plugin installation.

#### uninstall()
Runs during plugin uninstallation.

The functions **install()**, **uninstall()**, **register_commands()** are optional and not mandatory

<Note: both files must have the name `plugin.py` and `manifest.json` is necessary for the Dragon-Black system to find them by these names

### Create plugin easily
You can easily create a plugin using a tool included in Dragon-Black.
The plugin creation tool included in Dragon-Black helps you fill out the **manifest.json** file and the **plugin.py** file

### how it works
the plugin creation tool
requests the data required by `manifest.json` to create the plugin and reloads the **manifest.json** with the requested data. Also, a template is automatically created for the `plugin.py` file

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

>**Note:**
the automatic method saves you a lot of time


## Local Testing of a plugin
Dragon-Black allows you to test your plugin locally, this is necessary when you are developing the plugin because you need to do tests to ensure that the plugin works correctly
to install your plugin locally
you just need to pass the plugin path to Dragon-Black

```dragon
dragon install <plugin_path>
```
the plugin will be installed locally

## Plugin Distribution
to distribute your plugin in the official repository of the Dragon-Black plugin manager you must meet the following requirements

- **1 verify functionality:** test the plugin locally
- **2 verify files** verify that manifest.json contains all the data
- **3 verify names** verify that the files have the names manifest.json, and plugin.py

once you have everything in order go to the official plugin manager repository

[Dragon-Black-Plugins](https://github.com/Brais-Dev/Dragon-Black-Plugins)

once you are in the official repository
- **1 fork the repository**
- **2 create a new branch**
- **3 make a pull request**

> **Note** tutorials will be shared on the YouTube channel [Brais Moure](https://www.youtube.com/@Brais-Dev?si=NNuXTcjqGPGISetL)