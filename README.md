# Betweenness Centrality

Este projeto compara a implementação própria do algoritmo de **centralidade de intermediação** (Brandes) em grafos ponderados, presente em `graph_lib.py`, com a função equivalente do **NetworkX**.

O script principal é o `main.py`, que gera grafos de diferentes tipos (aleatórios, planar, ciclo, cadeia, completo e Barabási–Albert), atribui pesos aleatórios às arestas e verifica se o top 10% dos vértices mais centrais coincide entre as duas implementações.

---

## Instalação

1. **Clone ou baixe o repositório**:

   ```bash
   git clone https://github.com/PedroLucas63/betweenness-centrality
   cd betweenness-centrality
   ```

2. **Crie e ative um ambiente virtual (recomendado)**:

   * Com `venv`:

     ```bash
     python -m venv venv
     source venv/bin/activate   # Linux/macOS
     venv\Scripts\activate     # Windows
     ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

   O arquivo `requirements.txt` inclui:

   ```text
   networkx>=3.5
   ```

4. **Verifique se `graph_lib.py` está no mesmo diretório de `main.py`.**

---

## Uso

Execute o script de testes:

```bash
python main.py
```

Será exibido, para cada tipo de grafo:

* **SUCCESS** (em verde) quando o top 10% de vértices coincide em ambas implementações.
* **ERROR** (em vermelho) quando há divergência.
* Resumo por categoria e resultado final de quantos testes passaram.

---

## Estrutura de código

### graph_lib.py

Contém a implementação de:

* `Graph`:

  * Armazena grafo como *dict-of-dicts* (`vértice -> vizinho -> atributos`), suportando grafos direcionados e não direcionados.
  * Métodos para adicionar nós (`add_node`), arestas (`add_edge`), listar nós (`nodes`), arestas (`edges`), tamanho (`size`) e acesso a atributos via `G[u][v]['weight']`.

* `djikstra(graph, start)`:

  * Calcula distâncias mínimas a partir de um vértice `start` usando min-heap.
  * Retorna:

    * `orders`: ordem de finalização de cada nó.
    * `predecessors`: listas de antecessores em caminhos mínimos.
    * `paths`: contagem de quantos caminhos mínimos existem para cada nó.

* `brandes(graph)`:

  * Implementa o algoritmo de Brandes para **betweenness centrality** em grafos ponderados.

### main.py

* **Importa** `graph_lib` e `networkx`.
* **Converte** grafos do NetworkX para `graph_lib.Graph` (função `netx_to_graph_lib`).
* **Define** função de teste que compara top 10% de vértices mais centrais.
* **Gera** grafos de vários tipos via geradores do NetworkX:

  * Erdos–Rényi (esparso e denso).
  * Grid 2D (planar).
  * Cycle (cíclico).
  * Path (cadeia).
  * Complete (completo).
  * Barabási–Albert.
* **Atribui** pesos aleatórios entre 1 e 10.
* **Exibe** relatório de `SUCCESS` e `ERROR` colorido no terminal, com totais por categoria e geral.
