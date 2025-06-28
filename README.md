# Universe Engine

Um motor de exploração espacial procedural desenvolvido em Python com Pygame.

## Descrição

O Universe Engine é um motor 3D simples que gera um universo procedural infinito com estrelas. O jogador pode navegar pelo espaço usando controles de teclado e mouse.

## Características

- Geração procedural de estrelas
- Navegação 3D com controles de teclado e mouse
- Sistema de chunks para otimização de performance
- Interface simples e intuitiva
- Seleção de estrelas com informações detalhadas
- **Sistema de seeds personalizadas para consistência**

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

O Universe Engine agora suporta seeds personalizadas para garantir consistência na geração do universo. A mesma seed sempre gerará o mesmo universo.

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

### Teste de Consistência

Para verificar se as seeds estão funcionando corretamente:

```bash
python test_seed_consistency.py
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
│   │   │   ├── render.py    # Funções de renderização
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
│   ├── test_seed_consistency.py  # Teste de consistência
│   └── README.md          # Este arquivo
```

## Configuração

As configurações do jogo podem ser alteradas no arquivo `src/utils/config.py`:

- `WIDTH, HEIGHT`: Resolução da tela
- `FOV_DEG`: Campo de visão em graus
- `CHUNK_SIZE`: Tamanho de cada chunk
- `CHUNK_RADIUS`: Raio de chunks visíveis
- `STARS_PER_CHUNK`: Número de estrelas por chunk
- `MOVE_SPEED`: Velocidade de movimento
- `MOUSE_SENS`: Sensibilidade do mouse
- `GLOBAL_SEED`: Seed padrão para geração procedural
- `USE_CUSTOM_SEED`: Define se deve usar seed personalizada
- `CUSTOM_SEED`: Seed personalizada do usuário

## Desenvolvimento

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das suas mudanças
4. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 