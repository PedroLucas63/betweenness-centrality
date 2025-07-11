import argparse
import csv
import os
import time
import random
from dataset.load_graph import load_graph
from utils.utils import netx_to_graph_lib, remove_nodes
from plot.plot import plot_graph_with_removed, plot_SIR_comparison
from simulations.simulations import simulate_SIR
import lib.graph_lib as glib


def run_simulation(place: str, percent: float = 0.1, output_dir: str = 'output'):
   os.makedirs(output_dir, exist_ok=True)
   imgs_dir = os.path.join(output_dir, 'imgs')
   os.makedirs(imgs_dir, exist_ok=True)
   log_path = os.path.join(output_dir, 'log.txt')
   csv_path = os.path.join(output_dir, 'removed_nodes.csv')

   # 1. Load and convert graph
   with open(log_path, 'w') as log:
      log.write(f"Run simulation on: {place}\nPercent: {percent}\nStarted at {time.ctime()}\n")
   G_nx = load_graph(place, 'length')
   G = netx_to_graph_lib(G_nx)

   # Estatísticas de peso para SIR (usa 1.0 se não houver arestas ponderadas)
   weights = [attrs.get('weight', 1.0) for _, _, attrs in G.edges()]
   mean_weight = sum(weights) / len(weights) if weights else 1.0

   # 2. Compute centralities
   cb = glib.brandes(G)
   dc = glib.degree_centrality(G)

   # 3. Determine top sets
   total = G.size()
   k = max(1, int(total * percent))
   cb_top = [n for n,_ in sorted(cb.items(), key=lambda x: x[1], reverse=True)[:k]]
   dc_top = [n for n,_ in sorted(dc.items(), key=lambda x: x[1], reverse=True)[:k]]
   # mixed half-half
   k_half = max(1, k // 2)
   mixed_top = list(set(
      [n for n,_ in sorted(cb.items(), key=lambda x: x[1], reverse=True)[:k_half]] +
      [n for n,_ in sorted(dc.items(), key=lambda x: x[1], reverse=True)[:k_half]]
   ))

   # 4. Save removed nodes list
   with open(csv_path, 'w', newline='') as fcsv:
      writer = csv.writer(fcsv)
      writer.writerow(['scenario', 'node'])
      for node in cb_top:
         writer.writerow(['betweenness', node])
      for node in mixed_top:
         writer.writerow(['mixed', node])

   # 5. Plot scenarios
   plot_graph_with_removed(G_nx, cb_top, os.path.join(imgs_dir, 'removed_betweenness.png'))
   plot_graph_with_removed(G_nx, mixed_top, os.path.join(imgs_dir, 'removed_mixed.png'))

   # 6. Prepare graphs for SIR
   graphs = {
      'original': G,
      'no_betweenness': remove_nodes(G, cb_top),
      'no_mixed': remove_nodes(G, mixed_top)
   }
   # initial infected
   common = set(G.nodes())
   for g in graphs.values():
      common &= set(g.nodes())
   common = list(common)
   init_k = max(1, int(len(common) * 0.001))
   initial = random.sample(common, init_k)

   # 7. Run SIR and collect
   results = {}
   for name, graph in graphs.items():
      S, I, R, I_total = simulate_SIR(
         graph,
         steps=1000,
         mean_weight=mean_weight,
         infected_nodes=initial,
         min_days_infected=5,
         days_to_lose_immunity=180,
         verbose=False
      )
      results[name] = {'S': S, 'I': I, 'R': R, 'I_total': I_total}
      with open(log_path, 'a') as log:
         log.write(f"Scenario: {name}\nTotal infected: {I_total}\n")

   # 8. Plot SIR comparison
   plot_SIR_comparison(results, imgs_dir)
   with open(log_path, 'a') as log:
      log.write(f"Plots saved in {imgs_dir}\nFinished at {time.ctime()}\n")


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Run SIR simulations on a city graph')
   parser.add_argument('--place', required=True, help='Place name for graph download')
   parser.add_argument('--percent', type=float, default=0.1,
                     help='Percentage of top nodes to remove')
   parser.add_argument('--output', default='output', help='Output directory')
   args = parser.parse_args()
   run_simulation(args.place, args.percent, args.output)
