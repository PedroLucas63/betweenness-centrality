import osmnx as ox
import networkx as nx
import graph_lib as glib  

def load_natal_graph() -> glib.Graph:
    """
    Baixa o grafo da cidade de Natal-RN e converte para o formato graph_lib.
    """
    print("Baixando grafo...")
    # G_nx = ox.graph_from_place('Natal, Rio Grande do Norte, Brazil', network_type='drive')
    # G_nx = ox.graph_from_place('Ponta Negra, Natal, Rio Grande do Norte, Brazil', network_type='drive')
    G_nx = ox.graph_from_place('Lagoa Nova, Natal, Rio Grande do Norte, Brazil', network_type='drive')
    # ox.plot_graph(G_nx) # Plota o grafo 
    G_nx = nx.Graph(G_nx)  # Converte para grafo não dirigido


    # Garante que cada aresta tenha um peso (distância)
    for u, v, data in G_nx.edges(data=True):
        data['weight'] = data.get('length', 1.0)

    return netx_to_graph_lib(G_nx)

def netx_to_graph_lib(G: nx.Graph) -> glib.Graph:
    graph = glib.Graph(G.is_directed())
    for u in G.nodes():
        graph.add_node(u)
    for u, v, data in G.edges(data=True):
        graph.add_edge(u, v, weight=data['weight'])
    return graph

if __name__ == '__main__':
    G_natal = load_natal_graph()
    print(f"Grafo de Natal carregado com {G_natal.size()} nós e {len(G_natal.edges())} arestas.")
