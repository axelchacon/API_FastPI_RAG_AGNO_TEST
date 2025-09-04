# tests/conftest.py
import pytest
import sys
import os

# Añadir el directorio de la aplicación al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Puedes añadir fixtures globales aquí si los necesitas
