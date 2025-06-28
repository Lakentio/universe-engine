# Universe Engine

Um motor de exploração espacial procedural desenvolvido em Python com Pygame, otimizado para performance e com interface moderna.

## Descrição

O Universe Engine é um motor 3D avançado que gera um universo procedural infinito com estrelas. O jogador pode navegar pelo espaço usando controles de teclado e mouse, com sistema de otimização inteligente e interface moderna.

## Características

- **Geração procedural de estrelas** com seeds personalizadas
- **Navegação 3D fluida** com controles de teclado e mouse
- **Sistema de chunks otimizado** para performance máxima
- **Frustum Culling** para renderização eficiente
- **Interface moderna** com painéis transparentes e gradientes
- **Minimapa interativo** das estrelas próximas
- **Sistema de performance** com estatísticas em tempo real
- **Seleção de estrelas** com informações detalhadas
- **Fade de distância** para efeito visual realista

## Controles

- **WASD**: Movimento horizontal (frente/trás/esquerda/direita)
- **QE**: Movimento vertical (cima/baixo)
- **Mouse**: Rotação da câmera
- **Clique esquerdo**: Selecionar estrela
- **ESC**: Sair do jogo

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd universe-engine
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o jogo:
```bash
python run.py
```

## Seeds Personalizadas

O Universe Engine suporta seeds personalizadas para garantir consistência na geração do universo. A mesma seed sempre gerará o mesmo universo.

### Uso de Seeds

```bash
# Usar seed padrão
python run.py

# Usar seed personalizada
python run.py --seed "meu-universo-123"

# Ver seeds de exemplo
python run.py --list-seeds
```

### Seeds de Exemplo

- `meu-universo-123`
- `galaxia-andromeda`
- `sistema-solar-2024`
- `nebulosa-vermelha`
- `cluster-estelar`

## Testes e Performance

### Teste de Consistência
```bash
python test_seed_consistency.py
```

### Teste de Performance
```bash
python performance_test.py
```

## Estrutura do Projeto

```
universe-engine/
├── src/
│   ├── main.py          # Arquivo principal do jogo
│   │   ├── core/
│   │   │   ├── engine.py    # Lógica principal do motor
│   │   │   └── __init__.py
│   │   ├── rendering/
│   │   │   ├── render.py    # Funções de renderização e UI
│   │   │   └── __init__.py
│   │   └── utils/
│   │       ├── config.py    # Configurações do jogo
│   │       └── __init__.py
│   ├── assets/              # Recursos do jogo (futuro)
│   ├── docs/               # Documentação (futuro)
│   ├── tests/              # Testes (futuro)
│   ├── requirements.txt    # Dependências Python
│   ├── .gitignore         # Arquivos ignorados pelo Git
│   ├── run.py             # Script de execução com suporte a seeds
│   ├── performance_test.py # Teste de performance
│   └── README.md          # Este arquivo
```

## Configuração

As configurações do jogo podem ser alteradas no arquivo `src/utils/config.py`:

### Configurações Básicas
- `WIDTH, HEIGHT`: Resolução da tela
- `FOV_DEG`: Campo de visão em graus
- `CHUNK_SIZE`: Tamanho de cada chunk
- `CHUNK_RADIUS`: Raio de chunks visíveis
- `STARS_PER_CHUNK`: Número de estrelas por chunk
- `MOVE_SPEED`: Velocidade de movimento
- `MOUSE_SENS`: Sensibilidade do mouse
- `TARGET_FPS`: FPS alvo

### Configurações de Seeds
- `GLOBAL_SEED`: Seed padrão para geração procedural
- `USE_CUSTOM_SEED`: Define se deve usar seed personalizada
- `CUSTOM_SEED`: Seed personalizada do usuário

### Configurações de Performance
- `FRUSTUM_CULLING`: Ativa frustum culling para otimização
- `MAX_VISIBLE_STARS`: Limite máximo de estrelas renderizadas
- `LOD_DISTANCE`: Distância para Level of Detail
- `STAR_FADE_DISTANCE`: Distância para fade das estrelas

### Configurações de UI/HUD
- `UI_SCALE`: Escala da interface
- `UI_COLORS`: Paleta de cores da interface
- `UI_FONT_SIZE`: Tamanho da fonte
- `UI_PANEL_ALPHA`: Transparência dos painéis

## Otimizações Implementadas

### Performance
- **Frustum Culling**: Renderiza apenas estrelas visíveis pela câmera
- **Level of Detail**: Reduz detalhes de objetos distantes
- **Cache Inteligente**: Sistema de cache de chunks otimizado
- **Limite de Estrelas**: Controle do número máximo de estrelas renderizadas
- **Fade de Distância**: Efeito visual que melhora a performance

### Interface
- **Painéis Transparentes**: Interface moderna com transparência
- **Gradiente de Fundo**: Efeito visual espacial
- **Minimapa Interativo**: Visualização das estrelas próximas
- **Estatísticas em Tempo Real**: FPS, estrelas visíveis, chunks carregados
- **Cursor Melhorado**: Indicador visual mais preciso
- **Informações Detalhadas**: Painel completo de informações da estrela selecionada

## Desenvolvimento

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das suas mudanças
4. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 