"""
Here the information of the commands is stored
"""


def show_help():
    print("Dragon-Black")
    print("\nusage: dragon [-h] [--version] [--update]")
    print("\n-options-")

    print("  -h, --help       Show this help message and exit")
    print("  --version        Dragon-Black version")
    print("  --update         Update dragon black")
    print("  --update_change  Check changes in the update")
    print("  --create-plugin  Create a new plugin using the assistant")

def drg():
    print("drg 1.0.3 (dragon)")
    print("\nusage: drg [options] command")
    print("\n-options-")

    print("  install <package>     - Install specified packages.")
    print("  uninstall <package>   - Uninstall specified packages. Configuration files")
    print("  search <qery>         - Search package by query, for example by name or")
    print("  info <package>        - Get brief information about a package ")
    print("  update                - Dragon-Black update")

def plugin():
    print("plugin 1.0.0 (dragon)")
    print("\nusage: plugin [options] command")
    print("\n-options-")

    print("  install <source>      - Install plugin from local path or git URL.")
    print("  install <name>        - Install plugin from repository by name.")
    print("  uninstall <name>      - Uninstall specified plugin.")
    print("  list                  - List installed plugins.")
    print("  available             - List available plugins from repositories.")
    print("  search <query>        - Search for plugins in repositories by query.")
    print("  info <name>           - Get brief information about a plugin.")
    print("  update                - Update plugin repository information.")

def drg_install_error():
    print("drg install requires an argument <package> ejm [drg install <package>]")
    print("Use --help for available options")

def drg_search_error():
    print("drg search requires an argument <package> ejm [drg search <package>]")
    print("Use --help for available options")

def drg_info_error():
    print("drg info requires an argument <package> ejm [drg info <package>]")
    print("Use --help for available options")

def plugin_install_error():
    print("plugin install requires an argument <name or source> ejm [plugin install <name> or plugin install <url>]")
    print("Use --help for available options")

def plugin_search_error():
    print("plugin search requires an argument <query> ejm [plugin search <query>]")
    print("Use --help for available options")

def drg_argument_error(name_argument):
    print(f"Unknown argument: {name_argument}")
    print("Use --help for available options")