# Plugin de prueba para Dragon-Black
# Autor: Dragon-Black Community
# Descripción: Plugin de prueba para verificar la funcionalidad del repositorio de plugins

from typing import Dict, Callable
import os

def test_function():
    """
    Función principal de prueba
    """
    print("¡Hola desde el plugin de prueba!")
    print("Este plugin está funcionando correctamente.")
    print("Verificando la funcionalidad del repositorio de plugins...")

def show_info():
    """
    Muestra información sobre el plugin
    """
    print("Plugin de Prueba - Dragon-Black")
    print("Versión: 1.0.0")
    print("Autor: Dragon-Black Community")
    print("Función: Verificar la funcionalidad del repositorio de plugins")

"""
Función principal que se ejecuta cuando se llama al comando del plugin
"""
def main():
    test_function()

"""
Función que se ejecuta cuando se carga el plugin
"""
def install():
    print("Plugin de prueba cargado correctamente")

"""
Función que registra comandos adicionales del plugin
"""
def register_commands() -> Dict[str, Callable]:
    return {
        "testcmd": test_function,
        "test_info": show_info
    }