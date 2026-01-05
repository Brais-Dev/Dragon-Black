"""
Package management system for Dragon-Black
Handles installation, uninstallation, and searching of security tools
"""
import os
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class PackageManager:
    """Manages installation, uninstallation, and searching of packages"""

    def __init__(self):
        # Use absolute paths based on the script location
        base_dir = Path(__file__).parent.parent  # Go up from core/ to root
        self.packages_file = base_dir / "data" / "packages_list.txt"
        self.installed_file = base_dir / "data" / "installed_packages.json"
        self.packages_list = self._load_packages_list()
        self.installed_packages = self._load_installed_packages()
    
    def _load_packages_list(self) -> List[str]:
        """Load the list of available packages from file"""
        try:
            with open(self.packages_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Warning: {self.packages_file} not found")
            return []
    
    def _load_installed_packages(self) -> Dict[str, str]:
        """Load the list of installed packages from file"""
        try:
            with open(self.installed_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create file if it doesn't exist
            self._save_installed_packages({})
            return {}
    
    def _save_installed_packages(self, packages: Dict[str, str]) -> None:
        """Save the list of installed packages to file"""
        with open(self.installed_file, 'w', encoding='utf-8') as f:
            json.dump(packages, f, indent=2)
    
    def list_packages(self) -> List[str]:
        """Return the list of all available packages"""
        return self.packages_list
    
    def search_packages(self, keyword: str) -> List[str]:
        """Search for packages containing the keyword"""
        keyword = keyword.lower()
        return [pkg for pkg in self.packages_list if keyword in pkg.lower()]
    
    def is_installed(self, package_name: str) -> bool:
        """Check if a package is installed"""
        return package_name in self.installed_packages
    
    def install_package(self, package_name: str) -> Tuple[bool, str]:
        """
        Install a package (placeholder - actual installation would be handled by the packages module)
        
        Args:
            package_name: Name of the package to install
            
        Returns:
            Tuple of (success, message)
        """
        if package_name not in self.packages_list:
            return False, f"Package '{package_name}' not found in available packages"
        
        if self.is_installed(package_name):
            return False, f"Package '{package_name}' is already installed"
        
        try:
            # Add to installed packages
            self.installed_packages[package_name] = "installed"
            self._save_installed_packages(self.installed_packages)
            return True, f"Package '{package_name}' installed successfully"
        except Exception as e:
            return False, f"Failed to install package: {str(e)}"
    
    def uninstall_package(self, package_name: str) -> Tuple[bool, str]:
        """
        Uninstall a package
        
        Args:
            package_name: Name of the package to uninstall
            
        Returns:
            Tuple of (success, message)
        """
        if not self.is_installed(package_name):
            return False, f"Package '{package_name}' is not installed"
        
        try:
            # Remove from installed packages
            del self.installed_packages[package_name]
            self._save_installed_packages(self.installed_packages)
            return True, f"Package '{package_name}' uninstalled successfully"
        except Exception as e:
            return False, f"Failed to uninstall package: {str(e)}"
    
    def get_package_info(self, package_name: str) -> Optional[Dict[str, str]]:
        """
        Get information about a package
        
        Args:
            package_name: Name of the package
            
        Returns:
            Dictionary with package information or None if not found
        """
        if package_name not in self.packages_list:
            return None
        
        info = {
            "name": package_name,
            "installed": self.is_installed(package_name),
        }
        
        # Additional info could be added here if available in other files
        return info
    
    def get_installed_packages(self) -> Dict[str, str]:
        """Return the dictionary of installed packages"""
        return self.installed_packages.copy()
    
    def get_installation_status(self) -> Dict[str, List[str]]:
        """
        Get installation status summary
        
        Returns:
            Dictionary with 'installed' and 'available' lists
        """
        installed = list(self.installed_packages.keys())
        available = [pkg for pkg in self.packages_list if pkg not in self.installed_packages]
        
        return {
            "installed": installed,
            "available": available
        }


# Global package manager instance
package_manager = PackageManager()


def list_packages() -> List[str]:
    """List all available packages"""
    return package_manager.list_packages()


def search_packages(keyword: str) -> List[str]:
    """Search for packages containing the keyword"""
    return package_manager.search_packages(keyword)


def install_package(package_name: str) -> Tuple[bool, str]:
    """Install a package"""
    return package_manager.install_package(package_name)


def uninstall_package(package_name: str) -> Tuple[bool, str]:
    """Uninstall a package"""
    return package_manager.uninstall_package(package_name)


def get_package_info(package_name: str) -> Optional[Dict[str, str]]:
    """Get information about a package"""
    return package_manager.get_package_info(package_name)


def get_installed_packages() -> Dict[str, str]:
    """Get list of installed packages"""
    return package_manager.get_installed_packages()


def get_installation_status() -> Dict[str, List[str]]:
    """Get installation status"""
    return package_manager.get_installation_status()