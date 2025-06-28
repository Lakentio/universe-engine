#!/usr/bin/env python3
"""
Script de teste de FPS em tempo real
"""

import sys
import os
import time

# Adiciona o diretório src ao path do Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_fps():
    """Testa o FPS do sistema de renderização."""
    from core.engine import update_visible_stars, set_universe_seed
    from rendering.render import world_to_screen
    import utils.config
    
    print("=== Teste de FPS - Universe Engine ===\n")
    
    set_universe_seed("fps-test")
    
    # Simula posições de câmera
    cam_pos = [0, 0, 0]
    cam_rot = [0, 0]
    
    # Obtém estrelas visíveis
    visible_stars, _ = update_visible_stars(cam_pos, cam_rot)
    print(f"Estrelas carregadas: {len(visible_stars)}")
    
    # Testa renderização por 100 frames
    print("Testando renderização por 100 frames...")
    start_time = time.time()
    
    for frame in range(100):
        rendered = 0
        for star in visible_stars:
            screen_pos = world_to_screen(*star[:3], cam_pos, cam_rot)
            if screen_pos:
                rendered += 1
        
        if frame % 20 == 0:
            print(f"Frame {frame}: {rendered} estrelas renderizadas")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time_per_frame = total_time / 100
    estimated_fps = 1.0 / avg_time_per_frame
    
    print(f"\nResultados:")
    print(f"Tempo total: {total_time:.3f}s")
    print(f"Tempo médio por frame: {avg_time_per_frame*1000:.2f}ms")
    print(f"FPS estimado: {estimated_fps:.1f}")
    
    if estimated_fps >= 30:
        print("✅ Performance EXCELENTE!")
    elif estimated_fps >= 20:
        print("✅ Performance BOA!")
    elif estimated_fps >= 15:
        print("⚠️ Performance ACEITÁVEL")
    else:
        print("❌ Performance BAIXA")

if __name__ == "__main__":
    test_fps() 