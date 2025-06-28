import graph_lib as glib
import networkx as nx
import random

def netx_to_graph_lib(G: nx.Graph) -> glib.Graph:
   """
   Converte um networkx.Graph para um graph_lib.Graph

   Args:
       G (nx.Graph): Um grafo do networkx

   Returns:
       glib.Graph: Um grafo do graph_lib
   """
   graph = glib.Graph(G.is_directed())
   for u in G.nodes():
      graph.add_node(u)
   for u, v in G.edges():
      graph.add_edge(u, v, weight=G[u][v]['weight'])

   return graph

def graph_lib_to_netx(G: glib.Graph) -> nx.Graph:
   """
   Converte um graph_lib.Graph para um networkx.Graph

   Args:
       G (glib.Graph): Um grafo do graph_lib

   Returns:
       nx.Graph: Um grafo do networkx
   """
   G = nx.Graph() if not G.is_directed() else nx.DiGraph()
      
   for u in G.nodes():
      G.add_node(u)
   for u, v in G.edges():
      G.add_edge(u, v, weight=G[u][v]['weight'])

   return G

def test(G: nx.Graph) -> bool:
   """
   Função de teste dos algoritmos de centralidade de intermediação

   Args:
       G (nx.Graph): Um grafo do networkx

   Returns:
       bool: True se os algoritmos de centralidade de intermediação forem equivalentes
   """
   G_own = netx_to_graph_lib(G)
   
   cb_own = glib.brandes(G_own)
   cb_nx = nx.betweenness_centrality(G, normalized=False, weight='weight')
   
   k_top = max(1, len(G.nodes()) // 10)
   top_own = sorted(cb_own.items(), key=lambda x: x[1], reverse=True)[:k_top]
   top_nx = sorted(cb_nx.items(), key=lambda x: x[1], reverse=True)[:k_top]
   
   for i in range(k_top):
      if top_own[i][0] != top_nx[i][0]:
         return False
   return True

if __name__ == '__main__':
   print("=== Iniciando testes ===")

   # Define tipos de grafos e geradores
   graph_tests = {
      "Grafo Aleatório": [
         lambda: nx.erdos_renyi_graph(50, 0.1),
         lambda: nx.erdos_renyi_graph(50, 0.2),
         lambda: nx.erdos_renyi_graph(100, 0.3)
      ],
      "Grafo Planar (Grid 10x10)": [
         lambda: nx.grid_2d_graph(10, 10),
         lambda: nx.grid_2d_graph(8, 12),
         lambda: nx.grid_2d_graph(12, 12)
      ],
      "Grafo Ciclo": [
         lambda: nx.cycle_graph(30),
         lambda: nx.cycle_graph(25),
         lambda: nx.cycle_graph(45)
      ],
      "Grafo Cadeia": [
         lambda: nx.path_graph(30),
         lambda: nx.path_graph(40),
         lambda: nx.path_graph(100)
      ],
      "Grafo Completo": [
         lambda: nx.complete_graph(20),
         lambda: nx.complete_graph(15),
         lambda: nx.complete_graph(35)
      ],
      "Grafo Barabasi-Albert": [
         lambda: nx.barabasi_albert_graph(50, 3),
         lambda: nx.barabasi_albert_graph(60, 2),
         lambda: nx.barabasi_albert_graph(80, 4)
      ]
   }

   total_success = 0
   total_tests = 0

   for gtype, gens in graph_tests.items():
      print(f"- {gtype}:")
      success_count = 0
      for idx, gen in enumerate(gens, start=1):
         G = gen()
         for u, v in G.edges():
               G[u][v]['weight'] = random.randint(1, 10)
         ok = test(G)
         total_tests += 1
         if ok:
               success_count += 1
               print(f"  - Grafo {idx}: \033[92mSUCCESS\033[0m")
         else:
               print(f"  - Grafo {idx}: \033[91mERROR\033[0m")
      print(f"  - Result: [{success_count}/{len(gens)}]")
      total_success += success_count

   print(f"\n- Resultado final: [{total_success}/{total_tests}]")
