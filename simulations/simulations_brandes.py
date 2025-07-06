import matplotlib.pyplot as plt
import networkx as nx
import time
import random
import lib.graph_lib as glib  # Usa sua versão do algoritmo de Brandes
import os
import matplotlib as mpl

def save_graph_image(G, path, title='Grafo', node_size=30):
    pos = nx.spring_layout(G, seed=42, k=0.6)
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]

    # Normalização dos pesos
    max_weight = max(edge_weights)
    min_weight = min(edge_weights)
    norm_weights = [(w - min_weight) / (max_weight - min_weight) if max_weight > min_weight else 1 for w in edge_weights]
    edge_widths = [0.5 + 4.5 * nw for nw in norm_weights]

    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_size=node_size)

    edges = nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_weights,
        edge_cmap=plt.cm.plasma,
        edge_vmin=min_weight,
        edge_vmax=max_weight,
        width=0.8,  # sempre fina
        alpha=0.8
    )
    sampled_nodes = random.sample(list(G.nodes()), k=min(15, len(G)))
    labels = {n: str(n) for n in sampled_nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    plt.title(title)
    plt.axis('off')

    # Colorbar com axes explicitamente definidos
    sm = mpl.cm.ScalarMappable(cmap=plt.cm.plasma, norm=mpl.colors.Normalize(vmin=min_weight, vmax=max_weight))
    sm.set_array([])
    plt.colorbar(sm, ax=plt.gca(), label='Peso da Aresta')

    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()

    

def benchmark_brandes_custom(
    sizes: list,
    graph_type: str = 'erdos',
    num_repeats: int = 3,
    seed: int = 42,
    folder: str = 'imgs/brandes',
    save_img: bool = False
):
    random.seed(seed)
    results = {
        'sizes': [],
        'random_weights': []
    }

    for n in sizes:
        if graph_type == 'erdos':
            p = min(0.05, 10 / n)
            G_base = nx.erdos_renyi_graph(n, p, seed=seed)

        elif graph_type == 'barabasi':
            m = min(5, max(1, n // 20))
            G_base = nx.barabasi_albert_graph(n, m, seed=seed)

        elif graph_type == 'planar':
            side = int(n ** 0.5)
            G_base = nx.grid_2d_graph(side, side)
            G_base = nx.convert_node_labels_to_integers(G_base)

        elif graph_type == 'strogatz':
            k = min(6, n - 1)
            p = 0.3
            G_base = nx.watts_strogatz_graph(n, k, p, seed=seed)

        else:
            raise ValueError(f"Tipo de grafo '{graph_type}' não suportado.")

        # Pesos aleatórios
        G2 = G_base.copy()
        for u, v in G2.edges():
            G2[u][v]['weight'] = random.uniform(0.5, 10.0)

        if save_img and n < 500:
            subfolder = os.path.join(folder, graph_type)
            os.makedirs(subfolder, exist_ok=True)
            image_path = os.path.join(subfolder, f"n{n}_base.png")
            save_graph_image(G2, image_path, title=f'{graph_type.capitalize()} n={n} (com pesos)')
            print(f" → Imagem salva: {image_path}")


        # Mede tempo
        times_rand = []
        for _ in range(num_repeats):
            t0 = time.perf_counter()
            _ = glib.brandes(G2)
            t1 = time.perf_counter()
            times_rand.append(t1 - t0)

        avg_time = sum(times_rand) / len(times_rand)
        results['sizes'].append(n)
        results['random_weights'].append(avg_time)

        print(f"[{graph_type} | n={n}] -> Tempo médio = {avg_time:.4f}s")

    return results
