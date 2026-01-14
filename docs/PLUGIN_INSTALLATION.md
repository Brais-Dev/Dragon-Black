# Guide to Install Plugins in Dragon-Black CLI

## Introduction
Plugin installation is a quite simple process
you just need to know the **Dragon-Black** commands

### To install a plugin
```bash
plugin install <plugin>
```

**Dragon-Black** also allows you to install a plugin locally or from a specific URL by passing the URL or path

```bash
plugin install <path or url>
```

### To uninstall a plugin
```bash
plugin uninstall <plugin>
```

### To view information about a plugin
```bash
plugin info <plugin>
```

### To view installed plugins
```bash
plugin list
```

### To view available plugins in the plugin manager
```bash
plugin available
```

### To update a specific plugin
```bash
plugin update <plugin_name>
```

### To update all plugin repositories
```bash
plugin update
```

### To search for plugins
```bash
plugin search <query>
```

## New Features

### Dependency Management
Plugins can now specify dependencies in their `manifest.json` file. These dependencies will be installed automatically when the plugin is installed.

### Plugin Updates
- You can update a specific plugin using `plugin update <plugin_name>`
- The command `plugin update` without arguments updates the information of all plugin repositories

### Installation from Multiple Sources
Plugins can be installed from:
- Official repositories: `plugin install plugin_name`
- Git URLs: `plugin install https://github.com/user/plugin.git`
- Local directories: `plugin install /path/to/plugin`