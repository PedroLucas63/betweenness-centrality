import osmnx as ox
import networkx as nx

def load_natal_graph(weight_type: str = 'none') -> nx.MultiDiGraph:
    """
    Carrega o grafo de Natal-RN com pesos definidos no atributo 'weight'.

    Args:
        weight_type (str): 'length', 'travel_time', etc.

    Returns:
        nx.MultiDiGraph: Grafo multiaresta com dados geográficos completos e atributo 'weight' definido.
    """
    place = 'Natal, Rio Grande do Norte, Brazil'
    G = ox.graph_from_place(place, network_type='drive')

    if weight_type != 'none':
        if weight_type == 'bearing':
            G = ox.bearing.add_edge_bearings(G)
        elif weight_type == 'length':
            G = ox.distance.add_edge_lengths(G)
        elif weight_type == 'speed_kph':
            ox.distance.add_edge_lengths(G)
            G = ox.routing.add_edge_speeds(G)
        elif weight_type == 'travel_time':
            ox.distance.add_edge_lengths(G)
            ox.routing.add_edge_speeds(G)
            G = ox.routing.add_edge_travel_times(G)

        # Agora define 'weight' para cada aresta
        for u, v, k, data in G.edges(keys=True, data=True):
            if weight_type in data:
                data['weight'] = data[weight_type]
            else:
                data['weight'] = 1  # valor padrão se não existir o atributo escolhido

    else:
        # Se 'none', atribui peso padrão 1 em todas as arestas
        for u, v, k, data in G.edges(keys=True, data=True):
            data['weight'] = 1

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
