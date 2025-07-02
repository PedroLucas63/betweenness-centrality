import networkx as nx
import lib.graph_lib as glib  
from copy import deepcopy

def netx_to_graph_lib(G: nx.Graph) -> glib.Graph:
   """
   Converte um networkx.Graph (ou DiGraph/MultiDiGraph) para um graph_lib.Graph

   Args:
      G (nx.Graph): Um grafo do networkx (pode ser dirigido ou multigrafo)

   Returns:
      glib.Graph: Um grafo do graph_lib, com direção e pesos preservados
   """
   graph = glib.Graph(G.is_directed())

   # Adiciona os nós
   for u in G.nodes():
      graph.add_node(u)

   # Verifica se é multigrafo para iterar com chave
   if G.is_multigraph():
      # G.edges(keys=True, data=True) retorna u,v,k,data
      for u, v, k, data in G.edges(keys=True, data=True):
         weight = data.get('weight', 1.0)
         graph.add_edge(u, v, weight=weight)
   else:
      # Para grafos simples
      for u, v, data in G.edges(data=True):
         weight = data.get('weight', 1.0)
         graph.add_edge(u, v, weight=weight)

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
       weight = G[u][v]['weight'] if 'weight' in G[u][v] else 1.0
       G.add_edge(u, v, weight=weight)

   return G

def remove_nodes(G: glib.Graph, nodes: list) -> glib.Graph:
   """
   Remove vários vértices do grafo

   Args:
       G (glib.Graph): Grafo do graph_lib
       nodes (list): Lista de vértices a serem removidos

   Returns:
       glib.Graph: Grafo com os vértices removidos
   """
   G_copy = deepcopy(G)
   for node in nodes:
      G_copy.remove_node(node)

   return G_copy

def clip(x: float, min_val: float, max_val: float) -> float:
   """
   Limita o valor de x entre min_val e max_val

   Args:
       x (float): O valor a ser limitado
       min_val (float): O valor mínimo
       max_val (float): O valor máximo

   Returns:
       float: O valor limitado
   """
   return max(min(x, max_val), min_val)