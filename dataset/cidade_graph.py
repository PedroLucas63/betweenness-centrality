import osmnx as ox
import networkx as nx

def load_natal_graph(weight_type: str='none') -> nx.Graph:
    """
    Baixa o grafo da cidade de Natal-RN e converte para o formato networkx.
    
    Args:
        weight_type (str): Tipo de peso das arestas.
            Pode ser:
                - 'bearings': ângulo de direção entre dois nós (em graus).
                - 'lengths': comprimento das ruas (em metros).
                - 'grades': inclinação do segmento viário (subida/descida).
                - 'speeds': velocidade estimada da via (em km/h).
                - 'travel_times': tempo estimado de deslocamento (em segundos), calculado com base na velocidade.
                - 'none': não utiliza pesos; o grafo será não ponderado.

    Returns:
        nx.Graph: Grafo da cidade de Natal-RN

    Observação:
        Os dados utilizados são obtidos do OpenStreetMap via a biblioteca OSMnx.
        A escolha do tipo de peso afeta algoritmos como caminho mínimo ou análise de centralidade,
        pois altera a métrica utilizada nas arestas.
    """
    G_nx = ox.graph_from_place('Natal, Rio Grande do Norte, Brazil', network_type='drive')
    
    if weight_type != 'none':
        if weight_type == 'bearings':
            G_nx = ox.bearing.add_edge_bearings(G_nx)
        elif weight_type == 'lengths':
            G_nx = ox.distance.add_edge_lengths(G_nx)
        elif weight_type == 'grades':
            G_nx = ox.elevation.add_edge_grades(G_nx)
        elif weight_type == 'speeds':
            G_nx = ox.routing.add_edge_speeds(G_nx)
        elif weight_type == 'travel_times':
            G_nx = ox.routing.add_edge_travel_times(G_nx)
    else:
        G_nx = nx.Graph(G_nx)

    return G_nx

if __name__ == '__main__':
    G_natal = load_natal_graph('none')
    print(f"Grafo de Natal carregado com {G_natal.number_of_nodes()} nós e {G_natal.number_of_edges()} arestas.")
