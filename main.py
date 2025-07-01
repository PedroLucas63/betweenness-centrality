from dataset.cidade_graph import load_natal_graph
from utils.utils import netx_to_graph_lib, remove_nodes
from plot.plot import plot_graph, plot_times, plot_SIR_comparison
from simulations.simulations import simulate_SIR
import lib.graph_lib as glib
import time
import random

# Baixa o grafo de Natal-RN e salva a imagem
G = load_natal_graph('lengths')
plot_graph(G, 'imgs/natal.png', figsize=(20, 20), node_size=10)

# Converte para graph_lib
G = netx_to_graph_lib(G)

# Calcula a centralidade de intermediação e alavanca o tempo de execução
start_time = time.time()
cb = glib.brandes(G)
end_time = time.time()
cb_time = end_time - start_time

# Calcula a centralidade de grau e alavanca o tempo de execução
start_time = time.time()
dc = glib.degree_centrality(G)
end_time = time.time()
dc_time = end_time - start_time

# Imprime a comparação de tempos
algorithms = ['Brandes', 'Grau']
times = [cb_time, dc_time]
plot_times(algorithms, times, 'imgs/times.png')

# Pega os 10% de vértices mais centrais dos dois algoritmos e aleatórios
k = max(1, len(G.nodes()) // 10)
cb_top = sorted(cb.items(), key=lambda x: x[1], reverse=True)[:k]
dc_top = sorted(dc.items(), key=lambda x: x[1], reverse=True)[:k]
random_top = random.sample(G.nodes(), k)

# Remove os nós mais centrais dos algoritmos
graphs = {
   'Original': G,
   'Brandes': remove_nodes(G, [x[0] for x in cb_top]),
   'Grau': remove_nodes(G, [x[0] for x in dc_top]),
   'Random': remove_nodes(G, random_top)
}

# Define o dicionário de resultados
results = {}

# Simula o modelo SIR em todos os grafos
for name, graph in graphs.items():
   print(f"Simulando {name}")
   S_count, I_count, R_count = simulate_SIR(graph, steps=500, verbose=True)
   results[name] = {'S': S_count, 'I': I_count, 'R': R_count}
   
# Plota a evolução da infecção em todos os grafos
plot_SIR_comparison(results, 'imgs')