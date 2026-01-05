"""
Plugin manager module for Dragon-Black
Allows community to create and install custom security tools
"""
import os
import json
import importlib.util
import subprocess
import urllib.request
from pathlib import Path
from typing import Dict, List, Callable, Optional
from core.configuration_language import Translator


class PluginManager:
    """Manages plugins for Dragon-Black"""

    def __init__(self):
        self.app = Translator()
        self.plugins_dir = Path(__file__).parent.parent / "plugins"
        self.plugins_dir.mkdir(exist_ok=True)
        self.installed_plugins_file = self.plugins_dir / "installed_plugins.json"
        self.commands_json_path = Path(__file__).parent.parent / "data" / "command.json"
        self.plugin_repo_file = Path(__file__).parent.parent / "data" / "plugin_repo.json"
        self.plugins: Dict[str, dict] = {}
        self.commands: Dict[str, Callable] = {}
        self.command_handler = None  # Will be set from outside
        self._load_installed_plugins()
        
    def _load_installed_plugins(self):
        """Load installed plugins from file"""
        try:
            if self.installed_plugins_file.exists():
                with open(self.installed_plugins_file, 'r', encoding='utf-8') as f:
                    self.plugins = json.load(f)
            else:
                self.plugins = {}
        except Exception:
            self.plugins = {}
    
    def _save_installed_plugins(self):
        """Save installed plugins to file"""
        with open(self.installed_plugins_file, 'w', encoding='utf-8') as f:
            json.dump(self.plugins, f, indent=2)
    
    def _validate_plugin(self, plugin_path: Path) -> bool:
        """Validate that a plugin has the required structure"""
        try:
            # Check if plugin.py exists
            plugin_file = plugin_path / "plugin.py"
            if not plugin_file.exists():
                return False
            
            # Check if manifest.json exists
            manifest_file = plugin_path / "manifest.json"
            if not manifest_file.exists():
                return False
            
            # Validate manifest structure
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
                
            required_fields = ['name', 'version', 'author', 'description', 'main']
            for field in required_fields:
                if field not in manifest:
                    return False
                    
            return True
        except Exception:
            return False
    
    def install_plugin(self, plugin_path: str) -> bool:
        """Install a plugin from a local directory or URL"""
        try:
            plugin_dir = Path(plugin_path)
            
            if not plugin_dir.exists():
                # If it's a URL or git repo, clone it
                if plugin_path.startswith(('http://', 'https://', 'git@')):
                    return self._install_from_git(plugin_path)
                else:
                    print(self.app.t("error_package_not_found"))
                    return False
            
            if not self._validate_plugin(plugin_dir):
                print(self.app.get_error_message("invalid_plugin"))
                return False
            
            # Load manifest
            manifest_file = plugin_dir / "manifest.json"
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            plugin_name = manifest['name']
            target_dir = self.plugins_dir / plugin_name
            
            # Copy plugin to plugins directory
            if target_dir.exists():
                print(self.app.get_error_message("already_installed", plugin_name))
                return False
            
            import shutil
            shutil.copytree(plugin_dir, target_dir)
            
            # Register plugin
            self.plugins[plugin_name] = {
                'path': str(target_dir),
                'manifest': manifest,
                'installed': True
            }
            self._save_installed_plugins()
            
            print(self.app.get_error_message("success_installed", plugin_name))
            
            # Try to load the plugin
            self.load_plugin(plugin_name)
            
            return True
        except Exception as e:
            print(f"{self.app.t('enter_error')}: {str(e)}")
            return False
    
    def _install_from_git(self, git_url: str) -> bool:
        """Install a plugin from a git repository"""
        try:
            plugin_name = git_url.split('/')[-1].replace('.git', '')
            target_dir = self.plugins_dir / plugin_name
            
            if target_dir.exists():
                print(self.app.get_error_message("already_installed", plugin_name))
                return False
            
            subprocess.run(['git', 'clone', git_url, str(target_dir)], 
                          check=True, capture_output=True)
            
            if not self._validate_plugin(target_dir):
                # Clean up if validation fails
                import shutil
                shutil.rmtree(target_dir)
                print(self.app.get_error_message("invalid_plugin"))
                return False
            
            # Register plugin
            manifest_file = target_dir / "manifest.json"
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            self.plugins[plugin_name] = {
                'path': str(target_dir),
                'manifest': manifest,
                'installed': True
            }
            self._save_installed_plugins()
            
            print(self.app.get_error_message("success_installed", plugin_name))
            
            # Try to load the plugin
            self.load_plugin(plugin_name)
            
            return True
        except subprocess.CalledProcessError:
            print(self.app.get_error_message("failed_to_install_git", git_url))
            return False
        except Exception as e:
            print(f"{self.app.t('enter_error')}: {str(e)}")
            return False
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a specific plugin"""
        try:
            plugin_info = self.plugins.get(plugin_name)
            if not plugin_info:
                return False

            plugin_path = Path(plugin_info['path'])
            plugin_file = plugin_path / "plugin.py"

            if not plugin_file.exists():
                return False

            # Load the plugin module
            spec = importlib.util.spec_from_file_location(f"plugin_{plugin_name}", plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get plugin manifest to access the command name
            manifest_file = plugin_path / "manifest.json"
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)

            # Register plugin command if specified in manifest
            if 'command' in manifest:
                plugin_command = manifest['command']

                # Register in the commands.json file for autocompletion
                self._add_command_to_json(plugin_command)

                # Register the main plugin command to execute the default function
                main_func = None
                if hasattr(module, 'main'):
                    # If there's a main function, use it
                    main_func = module.main
                elif 'default_function' in manifest:
                    # If there's a default function specified in manifest
                    if hasattr(module, manifest['default_function']):
                        main_func = getattr(module, manifest['default_function'])
                else:
                    # If register_commands exists, register the first function or use a default approach
                    if hasattr(module, 'register_commands'):
                        commands = module.register_commands()
                        # Use the first function as the main command if no specific main is defined
                        if commands:
                            main_func = next(iter(commands.values()))

                # Register the command in both plugin manager and command handler
                if main_func:
                    self.commands[plugin_command] = main_func
                    # Register in the main command handler if available
                    if self.command_handler:
                        self.command_handler.add_command(plugin_command, main_func)

            # Register additional commands if they exist
            if hasattr(module, 'register_commands'):
                commands = module.register_commands()
                for cmd_name, cmd_func in commands.items():
                    # Register with plugin prefix for clarity
                    self.commands[f"plugin {plugin_name} {cmd_name}"] = cmd_func
                    # Also register directly if no conflict and add to JSON
                    if cmd_name not in self.commands:
                        self.commands[cmd_name] = cmd_func
                        self._add_command_to_json(cmd_name)
                        # Register in the main command handler if available
                        if self.command_handler:
                            self.command_handler.add_command(cmd_name, cmd_func)

            # If plugin has an install function, run it
            if hasattr(module, 'install'):
                module.install()

            return True
        except Exception as e:
            print(f"{self.app.t('enter_error')} {plugin_name}: {str(e)}")
            return False

    def _add_command_to_json(self, command: str):
        """Add a command to the commands.json file for autocompletion"""
        try:
            # Load existing commands
            if self.commands_json_path.exists():
                with open(self.commands_json_path, 'r', encoding='utf-8') as f:
                    commands = json.load(f)
            else:
                commands = []

            # Add command if it doesn't exist
            if command not in commands:
                commands.append(command)

                # Write back to file
                with open(self.commands_json_path, 'w', encoding='utf-8') as f:
                    json.dump(commands, f, indent=2)
        except Exception as e:
            print(f"Error adding command to JSON: {str(e)}")
    
    def load_all_plugins(self):
        """Load all installed plugins"""
        for plugin_name in self.plugins:
            if self.plugins[plugin_name].get('installed', False):
                self.load_plugin(plugin_name)
    
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Uninstall a plugin"""
        try:
            if plugin_name not in self.plugins:
                print(self.app.get_error_message("plugin_not_found", plugin_name))
                return False
            
            plugin_info = self.plugins[plugin_name]
            plugin_path = Path(plugin_info['path'])
            
            # Remove plugin directory
            import shutil
            shutil.rmtree(plugin_path)
            
            # Remove from registry
            del self.plugins[plugin_name]
            self._save_installed_plugins()
            
            # Remove commands associated with this plugin
            plugin_commands = [cmd for cmd in self.commands if cmd.startswith(f"plugin {plugin_name}")]
            for cmd in plugin_commands:
                del self.commands[cmd]
            
            print(self.app.get_error_message("success_uninstalled", plugin_name))
            return True
        except Exception as e:
            print(f"{self.app.t('enter_error')}: {str(e)}")
            return False
    
    def list_plugins(self) -> List[dict]:
        """List all installed plugins"""
        return [info for info in self.plugins.values()]
    
    def get_plugin_info(self, plugin_name: str) -> Optional[dict]:
        """Get information about a specific plugin"""
        return self.plugins.get(plugin_name)
    
    def handle_plugin_command(self, cmd: str) -> Optional[bool]:
        """Handle a plugin-related command"""
        if cmd.startswith("plugin install "):
            plugin_source = cmd[15:].strip()
            return self.install_plugin(plugin_source)
        
        elif cmd.startswith("plugin uninstall "):
            plugin_name = cmd[17:].strip()
            return self.uninstall_plugin(plugin_name)
        
        elif cmd == "plugin list":
            plugins = self.list_plugins()
            if plugins:
                print(f"{len(plugins)} {self.app.t('available_packages')}:")
                for plugin in plugins:
                    manifest = plugin.get('manifest', {})
                    name = manifest.get('name', 'Unknown')
                    desc = manifest.get('description', 'No description')
                    print(f"  - {name}: {desc}")
            else:
                print(self.app.t('no_results'))
            return True
        
        elif cmd.startswith("plugin info "):
            plugin_name = cmd[12:].strip()
            info = self.get_plugin_info(plugin_name)
            if info:
                manifest = info.get('manifest', {})
                print(f"{self.app.get_info_message('package_info')}: {manifest.get('name', 'Unknown')}")
                print(f"  {self.app.t('enter_description')}: {manifest.get('description', 'N/A')}")
                print(f"  {self.app.t('enter_version')}: {manifest.get('version', 'N/A')}")
                print(f"  {self.app.t('enter_author')}: {manifest.get('author', 'N/A')}")
                print(f"  Plugin repo  {manifest.get('git_url', 'N/A')}")
                print(f"  {self.app.t('enter_command')}: {manifest.get('command', 'N/A')}")
            else:
                print(self.app.get_error_message("plugin_not_found", plugin_name))
            return True
        
        # Check if it's a registered plugin command
        if cmd in self.commands:
            try:
                self.commands[cmd]()
                return True
            except Exception as e:
                print(f"{self.app.t('enter_error')}: {str(e)}")
                return False

        return None

    def _load_plugin_repo_config(self):
        """Load plugin repository configuration"""
        try:
            if self.plugin_repo_file.exists():
                with open(self.plugin_repo_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "repositories": [
                        {
                            "name": "community",
                            "url": "https://raw.githubusercontent.com/Brais-Dev/Dragon-Black-Plugins/main/plugins.json",
                            "description": "Repositorio de plugins de la comunidad"
                        }
                    ],
                    "local_plugins": []
                }
                with open(self.plugin_repo_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception:
            # Return default config if there's an error
            return {
                "repositories": [
                    {
                        "name": "community",
                        "url": "https://raw.githubusercontent.com/Brais-Dev/Dragon-Black-Plugins/main/plugins.json",
                        "description": "Repositorio de plugins de la comunidad"
                    }
                ],
                "local_plugins": []
            }

    def get_available_plugins(self) -> List[dict]:
        """Get list of available plugins from repositories"""
        config = self._load_plugin_repo_config()
        all_plugins = []

        # Add plugins from configured repositories
        for repo in config.get("repositories", []):
            try:
                # Fetch plugins from remote repository
                response = urllib.request.urlopen(repo["url"])
                repo_plugins = json.loads(response.read().decode())
                for plugin in repo_plugins:
                    plugin["repository"] = repo["name"]
                    all_plugins.append(plugin)
            except Exception as e:
                print(f"Error fetching plugins from {repo['name']}: {str(e)}")
                continue

        # Add local plugins from config
        for plugin in config.get("local_plugins", []):
            all_plugins.append(plugin)

        return all_plugins

    def search_available_plugins(self, keyword: str) -> List[dict]:
        """Search for plugins in repositories by keyword"""
        all_plugins = self.get_available_plugins()
        keyword = keyword.lower()
        return [
            plugin for plugin in all_plugins
            if keyword in plugin.get("name", "").lower() or
               keyword in plugin.get("description", "").lower()
        ]

    def install_plugin_from_repo(self, plugin_name: str) -> bool:
        """Install a plugin from the repository"""
        available_plugins = self.get_available_plugins()

        # Find the plugin in available plugins
        target_plugin = None
        for plugin in available_plugins:
            if plugin.get("name", "").lower() == plugin_name.lower():
                target_plugin = plugin
                break

        if not target_plugin:
            print(self.app.get_error_message("plugin_not_found", plugin_name))
            return False

        # Get the source URL or git repo from the plugin info
        source = target_plugin.get("source", target_plugin.get("git_url"))
        if not source:
            print(self.app.get_error_message("plugin_no_source_url", plugin_name))
            return False

        # Install the plugin from the source
        return self.install_plugin(source)

    def update_plugin_repos(self) -> bool:
        """Update plugin repository information"""
        try:
            config = self._load_plugin_repo_config()
            print(self.app.t("updating_plugin_repositories"))

            for repo in config.get("repositories", []):
                print(self.app.get_info_message("checking_repository", repo['name']))

            print(self.app.t("plugin_repositories_updated_successfully"))
            return True
        except Exception as e:
            print(self.app.get_error_message("error_updating_plugin_repositories", str(e)))
            return False


# Global plugin manager instance
plugin_manager = PluginManager()


def install_plugin(plugin_path: str) -> bool:
    """Install a plugin"""
    return plugin_manager.install_plugin(plugin_path)


def uninstall_plugin(plugin_name: str) -> bool:
    """Uninstall a plugin"""
    return plugin_manager.uninstall_plugin(plugin_name)


def list_plugins() -> List[dict]:
    """List installed plugins"""
    return plugin_manager.list_plugins()


def get_plugin_info(plugin_name: str) -> Optional[dict]:
    """Get plugin information"""
    return plugin_manager.get_plugin_info(plugin_name)


def handle_plugin_command(cmd: str) -> Optional[bool]:
    """Handle plugin commands"""
    return plugin_manager.handle_plugin_command(cmd)


def load_all_plugins():
    """Load all installed plugins"""
    plugin_manager.load_all_plugins()

def get_available_plugins() -> List[dict]:
    """Get list of available plugins from repositories"""
    return plugin_manager.get_available_plugins()

def search_available_plugins(keyword: str) -> List[dict]:
    """Search for plugins in repositories by keyword"""
    return plugin_manager.search_available_plugins(keyword)

def install_plugin_from_repo(plugin_name: str) -> bool:
    """Install a plugin from the repository"""
    return plugin_manager.install_plugin_from_repo(plugin_name)

def update_plugin_repos() -> bool:
    """Update plugin repository information"""
    return plugin_manager.update_plugin_repos()
