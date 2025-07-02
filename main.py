import time
import sys
import threading
import random

from dataset.cidade_graph import load_natal_graph
from utils.utils import netx_to_graph_lib, remove_nodes
from plot.plot import plot_graph, plot_times, plot_SIR_comparison, plot_graph_with_removed
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
      # Ao sair, imprime o total
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

   print('Carregando o grafo de Natal-RN...')
   with live_timer("load_natal_graph"):
      G_nx = load_natal_graph('length')
   plot_graph(G_nx, 'imgs/natal.png', figsize=(20, 20), node_size=10)
   print(" → imagem 'imgs/natal.png' gerada\n")

   print('Convertendo para graph_lib...')
   with live_timer("netx_to_graph_lib"):
      G = netx_to_graph_lib(G_nx)
   print()

   # Calcula peso médio
   weight_min = min(attrs['weight'] for _, _, attrs in G.edges())
   weight_max = max(attrs['weight'] for _, _, attrs in G.edges())
   total_weight = sum(attrs['weight'] for _, _, attrs in G.edges())
   edges_count = len(G.edges())
   mean_weight = total_weight / edges_count if edges_count else 0
   print(f'Grafo de Natal-RN com peso médio de {mean_weight:.2f}, entre {weight_min:.2f} e {weight_max:.2f} ({edges_count} arestas)\n')

   # Brandes
   print('Calculando centralidade de intermediação (Brandes)...')
   start_time = time.time()
   with live_timer("glib.brandes"):
      cb = glib.brandes(G)
   end_time = time.time()
   cb_time = end_time - start_time
   print(f"Brandes levou {cb_time:.2f}s\n")

   # Grau
   print('Calculando centralidade de grau...')
   start_time = time.time()
   with live_timer("glib.degree_centrality"):
      dc = glib.degree_centrality(G)
   end_time = time.time()
   dc_time = end_time - start_time
   print(f"Grau levou {dc_time:.2f}s\n")

   # Plota comparação de tempos
   algorithms = ['Brandes', 'Grau']
   times = [cb_time, dc_time]
   plot_times(algorithms, times, 'imgs/times.png')
   print("Comparação de tempos salva em 'imgs/times.png'\n")

   # Seleciona top 10% e gera subgrafos
   k = max(1, G.size() // 10)
   cb_top = sorted(cb.items(), key=lambda x: x[1], reverse=True)[:k]
   dc_top = sorted(dc.items(), key=lambda x: x[1], reverse=True)[:k]
   random_top = random.sample(list(G.nodes()), k)
   
   print('Plotando subgrafos...')
   plot_graph_with_removed(G_nx, [n for n, _ in cb_top],'imgs/brandes.png',figsize=(20, 20), node_size=10)
   plot_graph_with_removed(G_nx, [n for n, _ in dc_top], 'imgs/grau.png',figsize=(20, 20), node_size=10)
   plot_graph_with_removed(G_nx, random_top, 'imgs/random.png',figsize=(20, 20), node_size=10)
   print(" → imagens 'imgs/brandes.png', 'imgs/grau.png' e 'imgs/random.png' geradas\n")

   graphs = {
      'Original': G,
      'Brandes': remove_nodes(G, [n for n, _ in cb_top]),
      'Grau': remove_nodes(G, [n for n, _ in dc_top]),
      'Random': remove_nodes(G, random_top)
   }

   # Simulações SIR
   results = {}
   for name, graph in graphs.items():
      print(f"Simulando SIR em: {name}")
      S_count, I_count, R_count = simulate_SIR(
         graph,
         steps=1000,
         mean_weight=mean_weight,
         min_days_infected=5,
         days_to_lose_immunity=180,
         verbose=True
      )
      results[name] = {'S': S_count, 'I': I_count, 'R': R_count}
      print(f" → Simulação {name} concluída\n")

   # Plot final
   plot_SIR_comparison(results, 'imgs')
   print("Comparação SIR gerada em 'imgs/'")

if __name__ == "__main__":
   main()
