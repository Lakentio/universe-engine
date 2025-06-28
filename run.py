#!/usr/bin/env python3
"""
Script de execução do Universe Engine
"""

import sys
import os
import argparse

# Adiciona o diretório src ao path do Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def parse_arguments():
    """Parse argumentos de linha de comando."""
    parser = argparse.ArgumentParser(description='Universe Engine - Motor de exploração espacial procedural')
    parser.add_argument('--seed', '-s', type=str, help='Seed personalizada para geração do universo')
    parser.add_argument('--list-seeds', '-l', action='store_true', help='Lista algumas seeds de exemplo')
    return parser.parse_args()

def list_example_seeds():
    """Lista algumas seeds de exemplo."""
    print("Seeds de exemplo para o Universe Engine:")
    print("  --seed 'meu-universo-123'")
    print("  --seed 'galaxia-andromeda'")
    print("  --seed 'sistema-solar-2024'")
    print("  --seed 'nebulosa-vermelha'")
    print("  --seed 'cluster-estelar'")
    print("\nPara usar uma seed, execute:")
    print("  python run.py --seed 'sua-seed-aqui'")

if __name__ == "__main__":
    args = parse_arguments()
    
    if args.list_seeds:
        list_example_seeds()
        sys.exit(0)
    
    if args.seed:
        # Importa e configura a seed personalizada
        from utils.config import USE_CUSTOM_SEED, CUSTOM_SEED
        import utils.config
        
        # Atualiza a configuração com a seed fornecida
        utils.config.USE_CUSTOM_SEED = True
        utils.config.CUSTOM_SEED = args.seed
        print(f"Usando seed personalizada: '{args.seed}'")
    
    from main import main
    main() 