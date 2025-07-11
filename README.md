# Betweenness Centrality 📈

[![Download Latest Release](https://img.shields.io/badge/Download-Latest%20Release-brightgreen)](https://github.com/PedroLucas63/betweenness-centrality/releases)

Algoritmos e simulações de centralidade de intermediação (Brandes) e grau em grafos de ruas, com benchmarking, validação e modelagem SIR.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Demo (`main.py`)](#demo-mainpy)
  - [CLI de Simulação (`run_simulation.py`)](#cli-de-simulacao-runsimulationpy)
  - [Benchmark (`benchmark.py`)](#benchmark-benchmarkpy)
  - [Validação (`validate_brandes.py`)](#validacao-validate_brandespy)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction 🚀

Este projeto fornece implementações em Python para cálculo de centralidade de intermediação (betweenness) usando o algoritmo de Brandes, bem como centralidade de grau, além de:

- Comparação de desempenho entre algoritmos.
- Remoção de vértices por diferentes estratégias e análise de impacto.
- Simulações epidemiológicas SIR em grafos.

## Features 🌟

- **Brandes vs Degree**: Compara tempos de execução.
- **Cenários de Remoção**: 10% aleatório, 10% top grau, 10% top betweenness, mista 5%+5%.
- **Plotagem**: Imagens dos grafos originais e removidos.
- **SIR Simulation**: Curvas S, I, R e infectados acumulados.
- **Benchmark**: Testes com grafos Erdos-Rényi e planar.
- **Validação**: Confere ordem de centralidade contra `networkx`.

## Getting Started 🛠️

**Requisitos**: Python 3.13.3

1. Clone o repositório:

   ```bash
   git clone https://github.com/PedroLucas63/betweenness-centrality.git
   cd betweenness-centrality
   ```

2. Crie e ative um virtualenv (pode variar dependendo do `shell` utilizado):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```

3. Instale dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Usage 🎮

### Demo (`main.py`)

Executa um fluxo completo para o grafo de Natal (RN):

```bash
python main.py
```

- Gera `output/imgs/natal.png` (grafo).
- Compara tempos (`times.png`).
- Remove vértices e plota subgrafos.
- Plota contagem de nós restantes (`nodes_counts.png`).
- Simula SIR e salva curvas em `output/imgs/`.

### CLI de Simulação (`run_simulation.py`)

Ferramenta flexível para qualquer local e porcentagem:

```bash
python run_simulation.py --place "Natal, Rio Grande do Norte, Brazil" --percent 0.1 --output resultado
```

- `--place`: nome para download do grafo OSMnx.
- `--percent`: fração de nós a remover (padrão 0.1).
- `--output`: diretório de saída.

Arquivos gerados:

- `removed_nodes.csv`: lista de nós removidos por cenário.
- `log.txt`: totais de infectados e caminhos de imagens.
- `output_dir/imgs/`: imagens dos grafos e curvas SIR.

### Benchmark (`benchmark.py`)

```bash
python benchmark.py
```

Gera gráficos de desempenho em `output/imgs/brandes` comparando Brandes em grafos gerados.

### Validação (`validate_brandes.py`)

```bash
python validate_brandes.py
```

Compara sua implementação com a do NetworkX usando os 10% de vértices mais centrais.

## Project Structure 📁

```
betweenness-centrality/
├── benchmark.py
├── main.py
├── run_simulation.py
├── validate_brandes.py
├── dataset/load_graph.py
├── lib/graph_lib.py
├── simulations/simulations.py
├── utils/utils.py
├── plot/plot.py
├── requirements.txt
└── output/
    ├── imgs/
    ├── removed_nodes.csv
    └── log.txt
```

## Contributing 🤝

Contribuições são bem-vindas! Abra uma *issue* ou envie um *pull request*.

## License 📄

MIT License. Veja o arquivo [LICENSE](LICENSE).

## Contact 📧

Feito com ❤️ por Gabriel Victor e Pedro Lucas

Email: pedrolucas.jsrn@gmail.com e g.victor.silva01@gmail.com
