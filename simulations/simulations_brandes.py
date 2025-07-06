import matplotlib.pyplot as plt
import networkx as nx
import time
import random
import lib.graph_lib as glib  # Usa sua versão do algoritmo de Brandes

def save_graph_image(G, path, title='Grafo', node_size=30):
    pos = nx.spring_layout(G, seed=42, k=0.6)
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]

    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_size=node_size)
    nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.3, edge_color=edge_weights, edge_cmap=plt.cm.plasma)

    # Mostrar só alguns rótulos
    sampled_nodes = random.sample(list(G.nodes()), k=min(15, len(G)))
    labels = {n: str(n) for n in sampled_nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()

def benchmark_brandes_custom(
    sizes: list,
    graph_type: str = 'erdos',
    num_repeats: int = 5,
    seed: int = 42,
    folder: str = 'imgs/brandes'  # Pasta para salvar as imagens
):
    random.seed(seed)
    results = {
        'random_weights': []
    }
    num_repeats = 1

    for n in sizes:
        if graph_type == 'erdos':
            p = min(0.05, 10/n)
            G_base = nx.erdos_renyi_graph(n, p, seed=seed)
        elif graph_type == 'barabasi':
            m = min(5, max(1, n // 20))
            G_base = nx.barabasi_albert_graph(n, m, seed=seed)
        else:
            raise ValueError("Tipo de grafo não suportado.")

        # Salva grafo base
        # base_path = f"{folder}/{graph_type}_n{n}_base.png"
        # save_graph_image(G_base, base_path, title=f'{graph_type.capitalize()} n={n} (base)')

        # Pesos aleatórios
        G2 = G_base.copy()
        for u, v in G2.edges():
            G2[u][v]['weight'] = random.uniform(0.5, 10.0)

        times_rand = []
        for _ in range(num_repeats):
            t0 = time.perf_counter()
            _ = glib.brandes(G2)
            t1 = time.perf_counter()
            times_rand.append(t1 - t0)

        avg_time = sum(times_rand) / len(times_rand)
        results['random_weights'].append(avg_time)

        print(f"[n={n}] -> Tempo médio (pesos aleatórios) = {avg_time:.4f}s")
        print(f" → Resultados computados para '{graph_type}', n={n}")

    return results
