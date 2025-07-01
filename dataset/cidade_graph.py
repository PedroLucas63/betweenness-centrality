import osmnx as ox
import networkx as nx

def load_natal_graph(weight_type: str = 'none', directed: bool = True) -> nx.Graph:
    """
    Carrega o grafo de Natal-RN com pesos definidos no atributo 'weight'.

    Args:
        weight_type (str): 'length', 'travel_time', etc.
        directed (bool): Se True, retorna um DiGraph; senão, Graph (não-direcionado)

    Returns:
        nx.Graph or nx.DiGraph: Grafo com uma única aresta entre pares de nós.
    """
    place = 'Natal, Rio Grande do Norte, Brazil'
    G_multi = ox.graph_from_place(place, network_type='drive')

    # Etapa 1: adiciona atributos
    if weight_type != 'none':
        if weight_type == 'bearing':
            G_multi = ox.bearing.add_edge_bearings(G_multi)
        elif weight_type == 'length':
            G_multi = ox.distance.add_edge_lengths(G_multi)
        elif weight_type == 'speed_kph':
            ox.distance.add_edge_lengths(G_multi)
            G_multi = ox.routing.add_edge_speeds(G_multi)
        elif weight_type == 'travel_time':
            ox.distance.add_edge_lengths(G_multi)
            ox.routing.add_edge_speeds(G_multi)
            G_multi = ox.routing.add_edge_travel_times(G_multi)

    # Etapa 2: cria grafo simples (DiGraph ou Graph)
    G = nx.DiGraph() if directed else nx.Graph()

    for u, v, k, data in G_multi.edges(keys=True, data=True):
        # Define o peso
        weight = data.get(weight_type, 1)
        print(data)

        # Se já existe uma aresta entre u-v, mantém a de menor peso
        if G.has_edge(u, v):
            if weight < G[u][v]['weight']:
                G[u][v].update(weight=weight)
        else:
            G.add_edge(u, v, weight=weight)

    return G

if __name__ == '__main__':
    weight_type = 'speed_kph'       # Altere conforme necessário
    directed = True              # True = DiGraph, False = Graph
    G_natal = load_natal_graph(weight_type, directed)

    print(f"Grafo carregado com {G_natal.number_of_nodes()} nós e {G_natal.number_of_edges()} arestas.")

    print("\nAmostra de arestas com atributo 'weight':")
    count = 0
    for u, v, data in G_natal.edges(data=True):
        print(f"({u}, {v}) -> weight: {data.get('weight')}")
        count += 1
        if count >= 10:
            break
