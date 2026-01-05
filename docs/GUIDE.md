# Complete Guide on **Dragon-Black**

---

## Introduction
In this session, you will learn how to use this tool so you can enjoy and get the most out of Termux with this tool

---

## Introduction to Commands

Dragon-Black CLI provides a complete and professional command system for managing security, development, and automation tools. Commands are organized into logical categories that facilitate their use and understanding.

---

## System Commands

### Basic Commands

#### Start Dragon-Black CLI
```bash
dragon
```
Starts the interactive interface of Dragon-Black CLI with all its available functionalities.

#### Exit Dragon-Black CLI
```bash
exit
```
Closes the current Dragon-Black CLI session and returns to the Termux shell.

### System Information Commands

#### View Version
```bash
dragon --version
dragon -v
```
Displays the current version of Dragon-Black CLI installed on the system.

#### View General Help
```bash
dragon --help
dragon -h
```
Displays the general help system with a description of the main commands.

### Update Commands

#### Update Dragon-Black CLI
```bash
dragon --update
```
Updates Dragon-Black CLI to the latest version available in the official repository.

#### View Update Changes
```bash
dragon --update_change
```
Displays the changes included in the next available update.

### Development Commands

#### Create Plugin
```bash
dragon --create-plugin
```
Starts the interactive assistant to create a new plugin with the appropriate structure.

## Package Management Commands

---

Dragon-Black CLI uses the `drg` command as an abbreviation for Dragon-Black for package management. This system provides access to more than 200 security and development tools.

### Package Installation

#### Install Individual Package
```bash
drg install PACKAGE_NAME
```
Installs a specific package from the available catalog.

**Examples:**
```bash
drg install nmap
drg install metasploit
drg install sqlmap
```

### Package Search

#### Search Packages
```bash
drg search QUERY
```
Searches for available packages that match the search query.

**Examples:**
```bash
drg search security
drg search network
drg search scanner
```

### Package Information

#### View Package Information
```bash
drg info PACKAGE_NAME
```
Displays detailed information about a specific package, including description, dependencies, and installation status.

**Examples:**
```bash
drg info nmap
drg info metasploit
```

### Package Management

#### List Available Packages
```bash
drg list
```
Displays the complete list of packages available in the catalog.

#### Uninstall Packages
```bash
drg uninstall PACKAGE_NAME
```
Uninstalls a previously installed package.

**Examples:**
```bash
drg uninstall nmap
drg uninstall old_tool
```

### System Update

#### Update System
```bash
drg update
```
Updates the package management system and synchronizes with the official repository.

---

## Plugin Commands

### Plugin Installation

#### Install from Repository
```bash
plugin install PLUGIN_NAME
```
Installs a plugin from the official plugin repository.

**Examples:**
```bash
plugin install security_tool
plugin install network_analyzer
```

#### Install from Git URL
```bash
plugin install GIT_URL
```
Installs a plugin directly from a public Git repository.

**Examples:**
```bash
plugin install https://github.com/user/tool_plugin.git
plugin install https://gitlab.com/user/utility_plugin.git
```

#### Install from Local Directory
```bash
plugin install DIRECTORY_PATH
```
Installs a plugin from a local directory in the file system.

**Examples:**
```bash
plugin install ~/my_plugin
plugin install /path/to/plugin
```

### Plugin Management

#### List Installed Plugins
```bash
plugin list
```
Displays all plugins currently installed on the system.

#### View Plugin Information
```bash
plugin info PLUGIN_NAME
```
Displays detailed information about a specific plugin.

**Examples:**
```bash
plugin info security_tool
plugin info network_analyzer
```

#### Uninstall Plugin
```bash
plugin uninstall PLUGIN_NAME
```
Uninstalls a previously installed plugin.

**Examples:**
```bash
plugin uninstall old_plugin
plugin uninstall unnecessary_tool
```

### Plugin Repository

#### List Available Plugins
```bash
plugin available
```
Displays all plugins available in the configured repositories.

#### Search Plugins
```bash
plugin search QUERY
```
Searches for available plugins that match the search query.

**Examples:**
```bash
plugin search security
plugin search network
plugin search analysis
```

#### Update Repositories
```bash
plugin update
```
Updates the information of the available plugin repositories.

### Plugin Help
```bash
plugin --help
plugin -h
```
Displays specific help for plugin management commands.

## Customization Commands

### Theme Management

#### Change Theme (Interactive)
```bash
theme
```
Starts the interactive theme selector that allows visually choosing from the available themes.

#### List Available Themes
```bash
theme list
```
Displays all visual themes available for Dragon-Black CLI.

#### Set Specific Theme
```bash
theme set THEME_NAME
```
Sets a specific theme for the Dragon-Black CLI interface.

**Examples:**
```bash
theme set default
theme set dark_green
theme set matrix
```

#### View Current Theme Information
```bash
theme info
```
Displays information about the currently active theme.

### Statistics and Diagnostics

#### View Autocomplete Statistics
```bash
autocomplete stats
```
Displays statistics about the use of the autocomplete system, including used commands and frequency.

## Help and Diagnostic Commands

### General Help
```bash
dragon --help
dragon -h
```
Displays the general help system.

### Specific Command Help
```bash
drg --help
drg -h
```
Displays specific help for package management commands.

```bash
plugin --help
plugin -h
```
Displays specific help for plugin management commands.

---

## Uninstalling Dragon-Black
Uninstalling or removing **Dragon-Black** from Termux is easy
simply execute the following command
```bash
drg uninstall dragon
```