import time
import sys
import threading
import random

from dataset.cidade_graph import load_natal_graph
from utils.utils import netx_to_graph_lib, remove_nodes
from plot.plot import (
   plot_graph,
   plot_bars,
   plot_SIR_comparison,
   plot_graph_with_removed
)
from simulations.simulations import simulate_SIR
import lib.graph_lib as glib


class live_timer:
   """
   Context manager que exibe em tempo real:
   Descrição: XX.Xs
   até o bloco terminar, sem interferir nas suas variáveis de tempo.
   """
   def __init__(self, desc: str, interval: float = 0.2):
      self.desc = desc
      self.interval = interval
      self._stop = threading.Event()
      self._thread = threading.Thread(target=self._run, daemon=True)

   def _run(self):
      start = time.time()
      while not self._stop.is_set():
         elapsed = time.time() - start
         sys.stdout.write(f"\r{self.desc}: {elapsed:5.1f}s")
         sys.stdout.flush()
         time.sleep(self.interval)
      elapsed = time.time() - start
      sys.stdout.write(f"\r{self.desc} → concluído em {elapsed:.2f}s\n")
      sys.stdout.flush()

   def __enter__(self):
      self._thread.start()
      return self

   def __exit__(self, exc_type, exc_val, exc_tb):
      self._stop.set()
      self._thread.join()


def main():
   print(f'Graph Lib Version: {glib.__version__}\n')

   # Carrega o grafo
   print('Carregando o grafo de Natal-RN...')
   with live_timer("load_natal_graph"):
      G_nx = load_natal_graph('length')
   plot_graph(G_nx, 'imgs/extend/natal.png', figsize=(20, 20), node_size=10)
   print(" → imagem 'imgs/extend/natal.png' gerada\n")

   # Converte para graph_lib
   print('Convertendo para graph_lib...')
   with live_timer("netx_to_graph_lib"):
      G = netx_to_graph_lib(G_nx)
   print()

   # Estatísticas de peso
   weights = [attrs['weight'] for _, _, attrs in G.edges()]
   weight_min, weight_max = min(weights), max(weights)
   mean_weight = sum(weights) / len(weights) if weights else 0
   print(f'Grafo de Natal-RN com peso médio de {mean_weight:.2f}, entre {weight_min:.2f} e {weight_max:.2f} ({len(G.edges())} arestas)\n')

   # Centralidades
   print('Calculando centralidade de intermediação (Brandes)...')
   start_time = time.time()
   with live_timer("glib.brandes"):
      cb = glib.brandes(G)
   end_time = time.time()
   cb_time = end_time - start_time
   
   print('Calculando centralidade de grau...')
   start_time = time.time()
   with live_timer("glib.degree_centrality"):
      dc = glib.degree_centrality(G)
   print()
   end_time = time.time()
   dc_time = end_time - start_time
   
   plot_bars(['Brandes', 'Grau'], [cb_time, dc_time], 'Tempo de execução (s)', 'Comparação de centralidades', 'imgs/extend/times.png')
   

   # Define percentuais
   total_nodes = G.size()
   k10 = max(1, total_nodes // 10)   # 10%
   k5 = max(1, total_nodes // 20)    # 5%

   # Top sets
   cb_top_10 = [n for n, _ in sorted(cb.items(), key=lambda x: x[1], reverse=True)[:k10]]
   dc_top_10 = [n for n, _ in sorted(dc.items(), key=lambda x: x[1], reverse=True)[:k10]]
   cb_top_5 = [n for n, _ in sorted(cb.items(), key=lambda x: x[1], reverse=True)[:k5]]
   dc_top_5 = [n for n, _ in sorted(dc.items(), key=lambda x: x[1], reverse=True)[:k5]]

   # Estratégia mista: união dos top 5% de cada
   mixed_set = set(cb_top_5) | set(dc_top_5)
   mixed_top = list(mixed_set)

   # Random para comparação (10%)
   random_top = random.sample(list(G.nodes()), k10)

   # Plot subgrafos removidos
   print('Plotando subgrafos...')
   plot_graph_with_removed(G_nx, cb_top_10,  'imgs/extend/brandes_10.png', figsize=(20,20), node_size=10)
   plot_graph_with_removed(G_nx, dc_top_10,   'imgs/extend/grau_10.png',    figsize=(20,20), node_size=10)
   plot_graph_with_removed(G_nx, mixed_top,   'imgs/extend/mixed_10.png',   figsize=(20,20), node_size=10)
   plot_graph_with_removed(G_nx, random_top,  'imgs/extend/random_10.png',   figsize=(20,20), node_size=10)
   print(" → imagens de remoção salvas em 'imgs/extend/'\n")

   # Quanto restou em cada abordagem
   remaining_counts = {
      'Original':   total_nodes,
      'Brandes 10%': total_nodes - len(cb_top_10),
      'Grau 10%':   total_nodes - len(dc_top_10),
      'Mista 10%':   total_nodes - len(mixed_top),
      'Random 10%': total_nodes - len(random_top)
   }
   plot_bars(
      list(remaining_counts.keys()),
      list(remaining_counts.values()),
      'Nós',
      'Comparação de nós por abordagem',
      'imgs/extend/nodes_counts.png'
   )
   print(" → comparação de nós restantes salva em 'imgs/extend/nodes_counts.png'\n")

   # Simulações SIR
   graphs = {
      'Original': G,
      'Brandes 10%': remove_nodes(G, cb_top_10),
      'Grau 10%':   remove_nodes(G, dc_top_10),
      'Mista 10%':   remove_nodes(G, mixed_top),
      'Random 10%': remove_nodes(G, random_top)
   }
   results = {}
    
   # Interseção dos nós presentes em todos os grafos
   common_nodes = set(G.nodes())
   for graph in graphs.values():
      common_nodes &= set(graph.nodes())

   common_nodes = list(common_nodes)
   k = max(1, int(len(common_nodes) * 0.001))
   infected = random.sample(common_nodes, k)
    
   for name, graph in graphs.items():
      print(f"Simulando SIR em: {name}")
      S_count, I_count, R_count, I_total = simulate_SIR(
         graph,
         steps=1000,
         mean_weight=mean_weight,
         infected_nodes=infected,
         min_days_infected=5,
         days_to_lose_immunity=180,
         verbose=True
      )
      results[name] = {'S': S_count, 'I': I_count, 'R': R_count, 'I_total': I_total}
      print(f" → Simulação {name} concluída\n")

   # Plot final comparação SIR
   plot_SIR_comparison(results, 'imgs/extend')
   print("Comparação SIR gerada em 'imgs/extend/'")


if __name__ == "__main__":
   main()
