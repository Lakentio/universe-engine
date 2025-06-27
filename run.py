#!/usr/bin/env python3
"""
Script de execução do Universe Engine
"""

import sys
import os

# Adiciona o diretório src ao path do Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from main import main
    main() 