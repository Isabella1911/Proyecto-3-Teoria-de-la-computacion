#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ejecutar la GUI del Proyecto 3 - Teoría de la Computación
Cifrado César con Máquinas de Turing
"""

if __name__ == "__main__":
    try:
        from gui import main
        print("=" * 60)
        print("Iniciando GUI - Cifrado César con Máquinas de Turing")
        print("=" * 60)
        main()
    except ImportError as e:
        print("Error: No se pudo importar el módulo GUI")
        print(f"   Detalles: {e}")
        print("\nAsegúrate de que todos los archivos estén en su lugar:")
        print("   - gui.py")
        print("   - maquina/encoder_mt.py")
        print("   - maquina/decoder_mt.py")
        print("   - maquina/turing.py")
        input("\nPresiona Enter para salir...")
    except Exception as e:
        print(f"Error inesperado: {e}")
        input("\nPresiona Enter para salir...")
