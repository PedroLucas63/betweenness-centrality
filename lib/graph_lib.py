import heapq
from collections import defaultdict

from collections import defaultdict

class Graph:
   def __init__(self, is_directed=False):
      """
      Inicializa um grafo vazio, com dict-of-dicts para pesos.
      """
      self._adjacency_list = defaultdict(dict)
      self._is_directed = is_directed

   def add_node(self, node):
      """
      Adiciona um vértice ao grafo.

      Args:
         node (hashable): Vértice a ser adicionado.
      """
      self._adjacency_list.setdefault(node, {})
      
      
   def remove_node(self, node):
      """
      Remove um vértice do grafo.

      Args:
         node (hashable): Vértice a ser removido.
      """
      self._adjacency_list.pop(node, None)
      for neighbors in self._adjacency_list.values():
         neighbors.pop(node, None)

   def add_edge(self, node1, node2, weight=1.0):
      """ 
      Adiciona uma aresta (node1 -> node2) com peso.

      Args:
         node1, node2 (hashable): Vértices.
         weight (float): Peso da aresta.
         is_directed (bool): Se False, adiciona também node2->node1.
      """
      self.add_node(node1)
      self.add_node(node2)

      self._adjacency_list[node1][node2] = {'weight': weight}
      if not self._is_directed:
         self._adjacency_list[node2][node1] = {'weight': weight}

   def nodes(self) -> list:
      """
      Returns:
         list: lista de todos os vértices.
      """
      return list(self._adjacency_list.keys())

   def edges(self) -> list:
      """
      Returns:
         list of tuples (u, v, attrs): arestas com atributos.
      """
      return [
         (u, v, attrs)
         for u, neighbors in self._adjacency_list.items()
         for v, attrs in neighbors.items()
      ]
   
   def is_directed(self) -> bool:
      """
      Returns:
         bool: True se o grafo for dirigido, False se for não dirigido.
      """
      return self._is_directed

   def size(self) -> int:
      """
      Returns:
         int: número de vértices.
      """
      return len(self._adjacency_list)

   def __getitem__(self, node) -> dict:
      """
      Permite usar G[u][v] para acessar o dict de atributos da aresta.

      Returns:
         dict: atributos da aresta (por ex. {'weight': 3.2}).
      """
      return self._adjacency_list[node]

   
def djikstra(graph, start):
   """
   Encontra menores caminhos em grafo ponderado usando o algoritmo de Dijkstra

   Args:
       graph (Graph): Grafo
       start (str): Vértice de partida

   Returns:
       orders (list): Lista com a ordem de visitação (vértices conforme são 'finalizados')
       predecessors (dict): Dicionário onde cada vértice aponta para lista de antecessores em caminhos mínimos
       paths (dict): Dicionário com o número de caminhos mínimos de start até cada vértice
   """
   
   distances = {}
   predecessors = {}
   paths = {}

   for node in graph.nodes():
      distances[node] = float('inf')
      predecessors[node] = []
      paths[node] = 0

   distances[start] = 0
   paths[start] = 1

   orders = []
   visited = set()

   heap = [(0, start)]

   while heap:
      dist_u, u = heapq.heappop(heap)
      if dist_u > distances[u]:
         continue

      if u not in visited:
         orders.append(u)
         visited.add(u)

      for v, attrs in graph[u].items():
         w = attrs['weight']
         alt = distances[u] + w

         if alt < distances[v]:
               distances[v] = alt
               predecessors[v] = [u]
               paths[v] = paths[u]
               heapq.heappush(heap, (alt, v))
         elif alt == distances[v]:
               predecessors[v].append(u)
               paths[v] += paths[u]

   return orders, predecessors, paths

def brandes(graph):
   """
   Algoritmo de Brandes para grafos ponderados

   Args:
       graph (Graph): Grafo

   Returns:
       centrality (dict): Dicionário com a centralidade de cada vértice
   """
   centrality = {v: 0 for v in graph.nodes()}
   
   for s in graph.nodes():
      orders, predecessors, paths = djikstra(graph, s)
      
      contribution = {v: 0 for v in graph.nodes()}
      while orders:
         w = orders.pop()
         
         for v in predecessors[w]:
            contribution[v] += (paths[v]/paths[w]) * (1 + contribution[w])
         if w != s:
            centrality[w] += contribution[w]
            
   return centrality

def degree_centrality(graph: Graph) -> dict:
   return {v: len(graph[v]) for v in graph.nodes()}