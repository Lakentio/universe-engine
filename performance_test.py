#!/usr/bin/env python3
"""
Script de teste de performance para o Universe Engine
"""

import sys
import os
import time
import statistics

# Adiciona o diretório src ao path do Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_performance():
    """Testa a performance do sistema de renderização."""
    from core.engine import update_visible_stars, get_performance_stats, set_universe_seed
    from rendering.render import world_to_screen
    import utils.config
    
    print("=== Teste de Performance - Universe Engine ===\n")
    
    # Configurações de teste
    test_positions = [
        [0, 0, 0],
        [50, 0, 50],
        [100, 0, 100],
        [200, 0, 200],
        [500, 0, 500]
    ]
    
    test_rotations = [
        [0, 0],
        [0.5, 0.5],
        [1.0, 1.0]
    ]
    
    print("1. Testando geração de chunks...")
    set_universe_seed("performance-test")
    
    chunk_times = []
    for pos in test_positions:
        start_time = time.time()
        visible_stars, chunks_loaded = update_visible_stars(pos, [0, 0])
        end_time = time.time()
        
        chunk_time = (end_time - start_time) * 1000  # em ms
        chunk_times.append(chunk_time)
        
        print(f"   Posição {pos}: {len(visible_stars)} estrelas, {chunks_loaded} chunks, {chunk_time:.2f}ms")
    
    print(f"   Tempo médio: {statistics.mean(chunk_times):.2f}ms")
    print(f"   Tempo máximo: {max(chunk_times):.2f}ms")
    print(f"   Tempo mínimo: {min(chunk_times):.2f}ms")
    
    print("\n2. Testando frustum culling...")
    culling_times = []
    for pos in test_positions:
        for rot in test_rotations:
            start_time = time.time()
            visible_stars, _ = update_visible_stars(pos, rot)
            end_time = time.time()
            
            culling_time = (end_time - start_time) * 1000
            culling_times.append(culling_time)
            
            print(f"   Pos {pos}, Rot {rot}: {len(visible_stars)} estrelas visíveis, {culling_time:.2f}ms")
    
    print(f"   Tempo médio com culling: {statistics.mean(culling_times):.2f}ms")
    
    print("\n3. Testando renderização...")
    render_times = []
    visible_stars, _ = update_visible_stars([0, 0, 0], [0, 0])
    
    for _ in range(100):  # 100 frames de teste
        start_time = time.time()
        rendered_count = 0
        
        for star in visible_stars[:100]:  # Limita a 100 estrelas para teste
            screen_pos = world_to_screen(*star[:3], [0, 0, 0], [0, 0])
            if screen_pos:
                rendered_count += 1
        
        end_time = time.time()
        render_time = (end_time - start_time) * 1000
        render_times.append(render_time)
    
    print(f"   Estrelas renderizadas: {rendered_count}")
    print(f"   Tempo médio de renderização: {statistics.mean(render_times):.2f}ms")
    print(f"   FPS estimado: {1000 / statistics.mean(render_times):.1f}")
    
    print("\n4. Estatísticas de memória...")
    stats = get_performance_stats()
    print(f"   Chunks em cache: {stats['cache_size']}")
    print(f"   Total de estrelas: {stats['total_stars']}")
    print(f"   Uso de memória estimado: {stats['memory_usage_mb']:.1f} MB")
    
    print("\n5. Comparação de configurações...")
    
    # Teste com frustum culling desabilitado
    utils.config.FRUSTUM_CULLING = False
    start_time = time.time()
    visible_stars_no_culling, _ = update_visible_stars([0, 0, 0], [0, 0])
    time_no_culling = (time.time() - start_time) * 1000
    
    # Teste com frustum culling habilitado
    utils.config.FRUSTUM_CULLING = True
    start_time = time.time()
    visible_stars_with_culling, _ = update_visible_stars([0, 0, 0], [0, 0])
    time_with_culling = (time.time() - start_time) * 1000
    
    print(f"   Sem culling: {len(visible_stars_no_culling)} estrelas, {time_no_culling:.2f}ms")
    print(f"   Com culling: {len(visible_stars_with_culling)} estrelas, {time_with_culling:.2f}ms")
    print(f"   Melhoria: {((time_no_culling - time_with_culling) / time_no_culling * 100):.1f}%")
    
    print("\n=== Teste Concluído ===")

if __name__ == "__main__":
    test_performance() 