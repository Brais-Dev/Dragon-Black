"""
Command handler module for Dragon-Black
Provides a modular command system to replace extensive match statements
"""
import os
import sys
import subprocess 
import time
from pathlib import Path
from typing import Dict, Callable, Optional, Any
from modules import packages
from core import updater
from core import help_system
from core.configuration_language import Translator
from modules.prompt_manager import DragonPromptManager
from core.package_manager import (
    list_packages, search_packages, install_package,
    uninstall_package, get_package_info, get_installed_packages
)
from core.plugin_manager import (
    install_plugin, uninstall_plugin, list_plugins,
    get_plugin_info, handle_plugin_command, load_all_plugins,
    get_available_plugins, search_available_plugins, install_plugin_from_repo,
    update_plugin_repos
)


class CommandHandler:
    """Handles commands in a modular way"""

    def __init__(self):
        self.app = Translator()
        self.commands: Dict[str, Callable] = {}
        self._initialize_commands()
    
    def _initialize_commands(self) -> None:
        """Initialize all commands in the handler"""
        # Installation commands
        install_commands = {
            "drg install a-rat": packages.arat,
            "drg install adb-toolkit": packages.adbtk,
            "drg install aircrack-ng": packages.aircrackng,
            "drg install andro-zenmap": packages.androZenmap,
            "drg install androbugs": packages.androbugs,
            "drg install apktool": packages.apktool,
            "drg install archlinux": packages.archlinux,
            "drg install asu": packages.asu,
            "drg install astranmap": packages.astraNmap,
            "drg install atlas": packages.atlas,
            "drg install audit-couchdb": packages.audit_couchdb,
            "drg install auxile": packages.auxile,
            "drg install avpass": packages.avpass,
            "drg install baf": packages.baf,
            "drg install beanshell": packages.beanshell,
            "drg install billcypher": packages.billcypher,
            "drg install binploit": packages.binploit,
            "drg install binwalk": packages.binwalk,
            "drg install black-hydra": packages.black_hydra,
            "drg install blackbox": packages.blackbox,
            "drg install breacher": packages.breacher,
            "drg install brutal": packages.brutal,
            "drg install brutex": packages.brutex,
            "drg install btc2idr": packages.btc2idr,
            "drg install cast2video": packages.cast2video,
            "drg install ccgen": packages.ccgen,
            "drg install cfr": packages.cfr,
            "drg install chkrootkit": packages.chkrootkit,
            "drg install clamav": packages.clamav,
            "drg install clickbot": packages.clickbot,
            "drg install clickjacking": packages.clickjacking,
            "drg install cmseek": packages.cmseek,
            "drg install cmsmap": packages.cmsmap,
            "drg install commix": packages.commix,
            "drg install cookie-stealer": packages.cookiestealer,
            "drg install crawlbox": packages.crawlbox,
            "drg install credmap": packages.credmap,
            "drg install crips": packages.crips,
            "drg install crunch": packages.crunch,
            "drg install cupp": packages.cupp,
            "drg install cyberscan": packages.cyberscan,
            "drg install d-tect": packages.dtect,
            "drg install dbdat": packages.dbdat,
            "drg install ddcrypt": packages.ddcrypt,
            "drg install devploit": packages.devploit,
            "drg install dhcpig": packages.dhcpig,
            "drg install dkmc": packages.dkmc,
            "drg install dnsrecon": packages.dnsrecon,
            "drg install dos2unix": packages.dos2unix,
            "drg install dost-attack": packages.dostattack,
            "drg install dsss": packages.dsss,
            "drg install eagleeye": packages.eagleeye,
            "drg install easy-map": packages.easyMap,
            "drg install ecode": packages.ecode,
            "drg install encode": packages.ecode,
            "drg install ettercap": packages.ettercap,
            "drg install evil-url": packages.evilURL,
            "drg install exiftool": packages.exiftool,
            "drg install eyewitness": packages.eyewitness,
            "drg install f4k3": packages.f4k3,
            "drg install fade": packages.fade,
            "drg install fb-brute": packages.fbBrute,
            "drg install fbbrutex": packages.fbbrutex,
            "drg install fbvid": packages.fbvid,
            "drg install fedora": packages.fedora,
            "drg install fim": packages.fim,
            "drg install fl00d12": packages.fl00d12,
            "drg install fpcompiler": packages.fpcompiler,
            "drg install gathetool": packages.gathetool,
            "drg install gemail-hack": packages.gemailhack,
            "drg install ginf": packages.ginf,
            "drg install gloom-framework": packages.gloomframework,
            "drg install goblinwordgenerator": packages.goblinwordgenerator,
            "drg install goldeneye": packages.goldeneye,
            "drg install google": packages.google,
            "drg install gpstr": packages.gpstr,
            "drg install hac": packages.hac,
            "drg install hash-buster": packages.hash_buster,
            "drg install hash-generator": packages.hashgenerator,
            "drg install hashcat": packages.hashcat,
            "drg install hasher": packages.hasher,
            "drg install hasherdotid": packages.hasherdotid,
            "drg install hashid": packages.hashid,
            "drg install heroku": packages.heroku,
            "drg install hpb": packages.hpb,
            "drg install hping3": packages.hping3,
            "drg install hydra": packages.hydra,
            "drg install iconset": packages.iconset,
            "drg install iconv": packages.iconv,
            "drg install indonesian-wordlist": packages.indonesian_wordlist,
            "drg install infoga": packages.infoga,
            "drg install innoextract": packages.innoextract,
            "drg install inspy": packages.inspy,
            "drg install instahack": packages.instaHack,
            "drg install inther": packages.inther,
            "drg install jadx": packages.jadx,
            "drg install kali-linux": packages.nethunter,
            "drg install katak": packages.katak,
            "drg install knockmail": packages.knockmail,
            "drg install ko-dork": packages.kodork,
            "drg install kojawafft": packages.kojawafft,
            "drg install leaked": packages.leaked,
            "drg install lfisuite": packages.lfisuite,
            "drg install liteotp": packages.liteotp,
            "drg install lynis": packages.lynis,
            "drg install mac-lookup": packages.maclook,
            "drg install maigret": packages.maigret,
            "drg install makedeb": packages.makedeb,
            "drg install map-eye": packages.mapeye,
            "drg install maxsubdofinder": packages.maxsubdofinder,
            "drg install mediainfo": packages.mediainfo,
            "drg install metasploit": packages.metasploit,
            "drg install mongoaudit": packages.mongoaudit,
            "drg install mrsip": packages.mrsip,
            "drg install namechk": packages.namechk,
            "drg install nmap": packages.nmap,
            "drg install nosqlmap": packages.nosqlmap,
            "drg install numpy": packages.numpy,
            "drg install octave": packages.octave,
            "drg install osif": packages.osif,
            "drg install owscan": packages.owscan,
            "drg install pacman4console": packages.pacman4console,
            "drg install pandas": packages.pandas,
            "drg install parsero": packages.parsero,
            "drg install parrot": packages.parrot,
            "drg install passgencvar": packages.passgencvar,
            "drg install pdfinfo": packages.pdfinfo,
            "drg install phoneinfoga": packages.phoneinfoga,
            "drg install planetwork-ddos": packages.planetwork_ddos,
            "drg install pranayama": packages.pranayama,
            "drg install pret": packages.pret,
            "drg install pwned-or-not": packages.pwnedOrNot,
            "drg install pwnstar": packages.pwnstar,
            "drg install pybozocrack": packages.pybozocrack,
            "drg install pyinstxtractor": packages.pyinstxtractor,
            "drg install pyrit": packages.pyrit,
            "drg install quikfind": packages.quikfind,
            "drg install rang3r": packages.rang3r,
            "drg install readme": packages.readme,
            "drg install recon-dog": packages.reconDog,
            "drg install red-hawk": packages.red_hawk,
            "drg install routersploit": packages.routersploit,
            "drg install rshell": packages.rshell,
            "drg install sanlen": packages.sanlen,
            "drg install sh33ll": packages.sh33ll,
            "drg install shc": packages.shc,
            "drg install sherlock": packages.sherlock,
            "drg install sitebroker": packages.sitebroker,
            "drg install sleuthkit": packages.sleuthkit,
            "drg install slowloris": packages.slowloris,
            "drg install sn1per": packages.sn1per,
            "drg install snitch": packages.snitch,
            "drg install social-engineering": packages.social,
            "drg install socfish": packages.socfish,
            "drg install spazsms": packages.spazsms,
            "drg install spiderbot": packages.spiderbot,
            "drg install sqldump": packages.sqldump,
            "drg install sqliv": packages.sqliv,
            "drg install sqlmap": packages.sqlmap,
            "drg install sqlmate": packages.sqlmate,
            "drg install sqlscan": packages.sqlscan,
            "drg install steghide": packages.steghide,
            "drg install striker": packages.striker,
            "drg install stylemux": packages.stylemux,
            "drg install sudo": packages.sudo,
            "drg install tcpdump": packages.tcpdump,
            "drg install tekdefense": packages.tekdefense,
            "drg install termpyter": packages.termpyter,
            "drg install termux-pro": packages.termux_pro,
            "drg install tesseract": packages.tesseract,
            "drg install textr": packages.textr,
            "drg install tm-scanner": packages.tmscanner,
            "drg install torshammer": packages.torshammer,
            "drg install tshark": packages.tshark,
            "drg install txtool": packages.txtool,
            "drg install ubuntu": packages.ubuntu,
            "drg install uncompyle": packages.uncompyle,
            "drg install upx": packages.upx,
            "drg install userrecon": packages.userrecon,
            "drg install vbug": packages.vbug,
            "drg install vcrt": packages.vcrt,
            "drg install virustotal-cli": packages.virustotal,
            "drg install webdav": packages.webdav,
            "drg install webmassploit": packages.webmassploit,
            "drg install websploit": packages.websploit,
            "drg install weeman": packages.weeman,
            "drg install wifiphisher": packages.wifiphisher,
            "drg install wifite": packages.wifite,
            "drg install wordpress-scan": packages.wordpreSScan,
            "drg install wordpresscan": packages.wordpresscan,
            "drg install wpscan": packages.wpscan,
            "drg install xadmin": packages.xadmin,
            "drg install xattacker": packages.xattacker,
            "drg install xd3v": packages.xd3v,
            "drg install xerxes": packages.xerxes,
            "drg install xl-py": packages.xlPy,
            "drg install xpl-search": packages.xplsearch,
            "drg install xshell": packages.xshell,
            "drg install xss-payload-list": packages.xss_payload_list,
            "drg install xsstrike": packages.xsstrike,
            "drg install yara": packages.yara,
            "drg install zphisher": packages.zphisher,
        }
        
        # Other commands
        other_commands = {
            "fmb-brute": packages.fmbrute,
            "drg update": updater.update_repo,
            "drg list": self._list_packages,
            "languages": self.app.load_language,
            "drg search": self._search_packages,
            "drg info": self._package_info,
            "drg uninstall": self._uninstall_package,
            "plugin install": self._install_plugin,
            "plugin uninstall": self._uninstall_plugin,
            "plugin list": self._list_plugins,
            "plugin info": self._plugin_info,
        }
        
        # Combine all commands
        self.commands.update(install_commands)
        self.commands.update(other_commands)
    
    def _list_packages(self) -> None:
        """List all available packages"""
        file_packages = Path(__file__).parent.parent / "data"
        packages_file = file_packages / "packages.txt"

        with open(packages_file, 'r') as f:
            line = [line.strip() for line in f]
        for lines in line:
            print(f"- {line}")
    
    def _search_packages(self) -> None:
        """Search for packages"""
        keyword = input(f"{self.app.t('enter')} keyword to search for: ").strip()
        if not keyword:
            print(self.app.t("enter_error"))
            return

        results = search_packages(keyword)
        if results:
            print(f"{len(results)} {self.app.get_error_message('search_results', self.app.t('available_packages'), keyword)}:")
            for pkg in results:
                status = f" [{self.app.get_info_message('installed_packages')}]" if self._is_package_installed(pkg) else ""
                print(f"  - {pkg}{status}")
        else:
            print(f"{self.app.get_error_message('no_results', keyword)}")

    def _package_info(self) -> None:
        """Show package information"""
        package_name = input(f"{self.app.t('enter')} package name to get info for: ").strip()
        if not package_name:
            print(self.app.t("enter_error"))
            return

        info = get_package_info(package_name)
        if info:
            print(f"{self.app.get_info_message('package_info')}: {info['name']}")
            status = self.app.get_info_message('package_installed') if info['installed'] else self.app.get_info_message('package_not_installed')
            print(f"{self.app.t('enter')} {status}")
        else:
            print(f"{self.app.get_error_message('package_not_found', package_name)}")

    def _uninstall_package(self) -> None:
        """Uninstall a package"""
        package_name = input(f"{self.app.t('enter')} package name to uninstall: ").strip()
        if not package_name:
            print(self.app.t("enter_error"))
            return

        success, message = uninstall_package(package_name)
        print(message)

    def _is_package_installed(self, package_name: str) -> bool:
        """Check if a package is installed"""
        installed = get_installed_packages()
        return package_name in installed

    def _search_packages_with_keyword(self, keyword: str) -> None:
        """Search for packages with a specific keyword"""
        if not keyword:
            print(self.app.t("enter_error"))
            return

        results = search_packages(keyword)
        if results:
            print(f"{len(results)} {self.app.get_error_message('search_results', self.app.t('available_packages'), keyword)}:")
            for pkg in results:
                status = f" [{self.app.get_info_message('installed_packages')}]" if self._is_package_installed(pkg) else ""
                print(f"  - {pkg}{status}")
        else:
            print(f"{self.app.get_error_message('no_results', keyword)}")

    def _package_info_with_name(self, package_name: str) -> None:
        """Show package information for a specific package"""
        if not package_name:
            print(self.app.t("enter_error"))
            return

        info = get_package_info(package_name)
        if info:
            print(f"{self.app.get_info_message('package_info')}: {info['name']}")
            status = self.app.get_info_message('package_installed') if info['installed'] else self.app.get_info_message('package_not_installed')
            print(f"{self.app.t('enter')} {status}")
        else:
            print(f"{self.app.get_error_message('package_not_found', package_name)}")

    def _uninstall_package_with_name(self, package_name: str) -> None:
        """Uninstall a specific package"""
        if not package_name:
            print(self.app.t("enter_error"))
            return

        success, message = uninstall_package(package_name)
        print(message)

    def _install_plugin(self) -> None:
        """Install a plugin"""
        plugin_source = input(f"{self.app.t('enter')} plugin source (path or URL): ").strip()
        if not plugin_source:
            print(self.app.t("enter_error"))
            return

        success = install_plugin(plugin_source)
        if success:
            print(self.app.get_info_message('success_installed', "Plugin"))
        else:
            print(self.app.get_error_message('failed_to_install_plugin'))

    def _uninstall_plugin(self) -> None:
        """Uninstall a plugin"""
        plugin_name = input(f"{self.app.t('enter')} plugin name to uninstall: ").strip()
        if not plugin_name:
            print(self.app.t("enter_error"))
            return

        success = uninstall_plugin(plugin_name)
        if success:
            print(self.app.get_info_message('success_uninstalled', "Plugin"))
        else:
            print(self.app.get_error_message('failed_to_uninstall_plugin'))

    def _list_plugins(self) -> None:
        """List all installed plugins"""
        plugins = list_plugins()
        if plugins:
            print(f"{len(plugins)} {self.app.t('installed_packages')}:")
            for plugin in plugins:
                manifest = plugin.get('manifest', {})
                name = manifest.get('name', 'Unknown')
                desc = manifest.get('description', 'No description')
                print(f"  - {name}: {desc}")
        else:
            print(f"0 {self.app.t('installed_packages')}")

    def _list_available_plugins(self) -> None:
        """List all available plugins from repositories"""
        plugins = get_available_plugins()
        if plugins:
            print(f"{len(plugins)} {self.app.t('available_packages')}:")
            for plugin in plugins:
                name = plugin.get('name', 'Unknown')
                desc = plugin.get('description', 'No description')
                repo = plugin.get('repository', 'Unknown')
                print(f"  - {name}: {desc} [Repo: {repo}]")
        else:
            print(f"0 {self.app.t('available_packages')}")

    def _plugin_info(self) -> None:
        """Show plugin information"""
        plugin_name = input(f"{self.app.t('enter')} plugin name to get info for: ").strip()
        if not plugin_name:
            print(self.app.t("enter_error"))
            return

        info = get_plugin_info(plugin_name)
        if info:
            manifest = info.get('manifest', {})
            print(f"{self.app.get_info_message('package_info')}: {manifest.get('name', 'Unknown')}")
            print(f"  {self.app.t('enter_description')}: {manifest.get('description', 'N/A')}")
            print(f"  {self.app.t('enter_version')}: {manifest.get('version', 'N/A')}")
            print(f"  {self.app.t('enter_author')}: {manifest.get('author', 'N/A')}")
        else:
            print(f"{self.app.get_error_message('plugin_not_found', plugin_name)}")

    def _search_available_plugins_with_keyword(self, keyword: str) -> None:
        """Search for available plugins with a specific keyword"""
        if not keyword:
            print(self.app.t("enter_error"))
            return

        results = search_available_plugins(keyword)
        if results:
            print(f"{len(results)} {self.app.get_error_message('search_results', self.app.t('available_packages'), keyword)}:")
            for plugin in results:
                name = plugin.get('name', 'Unknown')
                desc = plugin.get('description', 'No description')
                repo = plugin.get('repository', 'Unknown')
                print(f"  - {name}: {desc} [Repo: {repo}]")
        else:
            print(f"{self.app.get_error_message('no_results', keyword)}")

    def handle_command(self, cmd: str) -> Optional[str]:
        """
        Handle a command and return the result

        Args:
            cmd: Command string to handle

        Returns:
            'exit' if exit command, True if handled, None if not found
        """
        # Special commands that need custom handling
        if cmd == "exit":
            return "exit"
        
        # =====drg abreviatuon
        if cmd == "drg":
            help_system.drg()
            return True

        elif cmd == "drg --help" or cmd == "drg -h":
            help_system.drg()
            return True

        elif cmd == "plugin --help" or cmd == "plugin -h":
            help_system.plugin()
            return True

        elif cmd == "drg install":
            help_system.drg_install_error()
            return True

        elif cmd == "drg search":
            help_system.drg_search_error()
            return True

        elif cmd == "drg info":
            help_system.drg_info_error()
            return True
       
        elif cmd == "plugin":
            help_system.plugin()
            return True
            
        elif cmd == "plugin install":
            help_system.plugin_install_error()
            return True

        elif cmd == "plugin search":
            help_system.plugin_search_error()
            return True
       
        elif cmd == "drg uninstall dragon":
            print(self.app.t("dragon_eliminate"))
            opc = input(self.app.t("enter_eliminate")).strip()
            if opc == "y":
                print("wait...")
                time.sleep(3)
                subprocess.run("rm -rf ~/.dragon", shell=True)
                subprocess.run("rm -rf $PREFIX/dragon", shell=True)
                print("Dragon-black was eliminated")
                sys.exit(0)
                

        # Handle commands with parameters first to ensure proper routing
        if cmd.startswith("plugin install "):
            plugin_source = cmd[15:]  # Get the plugin source after "plugin install "

            # Check if it's a local path first
            plugin_path = Path(plugin_source)

            if plugin_path.exists():
                # It's a local path, install directly
                success = install_plugin(plugin_source)
                if success:
                    print(self.app.get_info_message('success_installed', f"Plugin from local path '{plugin_source}'"))
                else:
                    print(self.app.get_error_message('failed_to_install_plugin'))
            else:
                # It's not a local path, try to install from repository
                success = install_plugin_from_repo(plugin_source)
                if success:
                    print(self.app.get_info_message('success_installed', f"Plugin '{plugin_source}' from repository"))
                else:
                    print(self.app.get_error_message('failed_to_install_from_repository', plugin_source))
            return True

        if cmd.startswith("plugin search "):
            keyword = cmd[14:]  # Get the keyword after "plugin search "
            self._search_available_plugins_with_keyword(keyword)
            return True

        elif cmd.startswith("plugin "):
            # Handle plugin commands
            result = handle_plugin_command(cmd)
            if result is not None:
                return result

        if cmd == "plugin available":
            self._list_available_plugins()
            return True

        if cmd == "plugin update":
            success = update_plugin_repos()
            if success:
                print(self.app.t("plugin_repositories_updated_successfully"))
            else:
                print(self.app.t("failed_to_update_plugin_repositories"))
            return True


        # Handle commands with parameters
        if cmd.startswith("drg search "):
            keyword = cmd[11:]  # Get the keyword after "drg search "
            self._search_packages_with_keyword(keyword)
            return True

        if cmd.startswith("drg info "):
            package_name = cmd[9:]  # Get the package name after "drg info "
            self._package_info_with_name(package_name)
            return True

        if cmd.startswith("drg uninstall "):
            package_name = cmd[14:]  # Get the package name after "drg uninstall "
            self._uninstall_package_with_name(package_name)
            return True

        if cmd.startswith("drg install "):
            package_name = cmd[12:]  # Get the package name after "drg install "
            # This is handled via the packages module
            install_cmd = f"drg install {package_name}"
            if install_cmd in self.commands:
                try:
                    self.commands[install_cmd]()
                    return True
                except Exception as e:
                    print(self.app.get_error_message('error_installing_package', f"{package_name}: {str(e)}"))
            else:
                print(self.app.get_error_message('package_not_available'))
                return False

        # Check if command exists in our registry
        if cmd in self.commands:
            try:
                self.commands[cmd]()
                return True
            except Exception as e:
                print(self.app.get_error_message('error_executing_command', f"{cmd}: {str(e)}"))
                return False

        return None  # Command not recognized
    
    def add_command(self, name: str, handler: Callable) -> None:
        """Add a new command to the handler"""
        self.commands[name] = handler
    
    def remove_command(self, name: str) -> bool:
        """Remove a command from the handler if it exists"""
        if name in self.commands:
            del self.commands[name]
            return True
        return False
    
    def get_available_commands(self) -> list:
        """Get list of all available commands"""
        return list(self.commands.keys())
    
    def command_exists(self, cmd: str) -> bool:
        """Check if a command exists"""
        return cmd in self.commands
