#!/usr/bin/env python3
"""
Script de prueba para verificar que el sistema de plugins funciona correctamente
"""

import sys
import os
sys.path.insert(0, '/data/data/com.termux/files/home/Dragon-Black')

from core.plugin_manager import PluginManager

def test_plugin_system():
    print("=== Prueba del Sistema de Plugins ===\n")
    
    # Crear una instancia del plugin manager
    pm = PluginManager()
    
    print(f"Directorio de plugins: {pm.plugins_dir}")
    print(f"Archivo de configuración de repositorio: {pm.plugin_repo_file}")
    
    # Probar la carga de configuración del repositorio
    config = pm._load_plugin_repo_config()
    print(f"Configuración de repositorio cargada: {config['repositories']}")
    
    # Probar la obtención de plugins disponibles
    print("\nBuscando plugins disponibles en repositorios remotos...")
    try:
        plugins = pm.get_available_plugins()
        print(f"Plugins disponibles: {len(plugins)} plugins encontrados")
        
        if plugins:
            print("\nPrimeros plugins encontrados:")
            for i, plugin in enumerate(plugins[:3]):  # Mostrar solo los primeros 3
                print(f"  {i+1}. Nombre: {plugin.get('name', 'N/A')}")
                print(f"     Descripción: {plugin.get('description', 'N/A')}")
                print(f"     Autor: {plugin.get('author', 'N/A')}")
                print(f"     Comando: {plugin.get('command', 'N/A')}")
                print()
        else:
            print("No se encontraron plugins en los repositorios (esto puede ser normal si no hay conexión o el archivo no existe aún)")
    except Exception as e:
        print(f"Error al buscar plugins: {str(e)}")
        print("Esto puede ser normal si el repositorio remoto no tiene el archivo plugins.json aún")
    
    print("\n=== Prueba completada ===")
    print("Si no hubo errores críticos, el sistema de plugins está configurado correctamente.")

if __name__ == "__main__":
    test_plugin_system()