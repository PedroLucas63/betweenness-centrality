import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import networkx as nx
import osmnx as ox
import os

def plot_SI(original, modificado, save_path: str = None):
    """
    Plota a evolução da infecção em um modelo SI, comparando antes e depois da remoção dos hubs.

    Args:
        original (list): Série temporal com número de infectados na rede completa.
        modificado (list): Série temporal com número de infectados após a remoção de hubs.
        save_path (str, optional): Caminho para salvar o gráfico. Se None, apenas exibe.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(original, label="Antes (rede completa)", color='blue', marker='o')
    plt.plot(modificado, label="Depois (hubs removidos)", color='red', marker='x')
    plt.xlabel("Iterações")
    plt.ylabel("Número de infectados")
    plt.title("Simulação de Pandemia - Evolução da Infecção (Modelo SI)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()


def plot_SIR(S_before, I_before, R_before, S_after, I_after, R_after, save_path: str = None):
    """
    Plota e compara a evolução de um modelo SIR antes e depois da remoção dos hubs.

    Args:
        S_before, I_before, R_before (list): Dados da simulação SIR na rede completa.
        S_after, I_after, R_after (list): Dados da simulação SIR com hubs removidos.
        save_path (str, optional): Caminho base para salvar os gráficos. Se None, apenas exibe.
    """
    # Gráfico comparando apenas infectados
    plt.figure(figsize=(10, 6))
    plt.plot(I_before, label='Infectados - Antes (rede completa)', color='red', linestyle='-')
    plt.plot(I_after, label='Infectados - Depois (hubs removidos)', color='purple', linestyle='--')
    plt.xlabel('Iterações')
    plt.ylabel('Número de Infectados')
    plt.title('Comparação da Infecção - Antes vs Depois da Remoção de Hubs (Modelo SIR)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(f"{save_path}_infectados.png", dpi=300)
    else:
        plt.show()

    # Gráfico completo com S, I, R
    plt.figure(figsize=(10, 6))
    plt.plot(S_before, label='Suscetíveis - Antes', color='blue', linestyle='-')
    plt.plot(I_before, label='Infectados - Antes', color='red', linestyle='-')
    plt.plot(R_before, label='Recuperados - Antes', color='green', linestyle='-')

    plt.plot(S_after, label='Suscetíveis - Depois', color='blue', linestyle='--')
    plt.plot(I_after, label='Infectados - Depois', color='red', linestyle='--')
    plt.plot(R_after, label='Recuperados - Depois', color='green', linestyle='--')

    plt.xlabel('Iterações')
    plt.ylabel('Número de Indivíduos')
    plt.title('Comparativo Completo - Modelo SIR (Antes vs Depois da Remoção de Hubs)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(f"{save_path}_sir_completo.png", dpi=300)
    else:
        plt.show()

def plot_bars(names, values, ylabel, title, save_path: str = None):
    """
    Gera um gráfico de barras comparando de diferentes opções.

    Args:
        names (list of str): Lista com os nomes das barras.
        values (list of float): Valores de cada barra.
        title (str): Título do gráfico.
        save_path (str, optional): Caminho para salvar o gráfico. Se None, o gráfico será exibido.
    """
    assert len(names) == len(values), "Listas 'names' e 'values' devem ter o mesmo tamanho."

    plt.figure(figsize=(8, 5))
    bars = plt.bar(names, values, color=['#4e79a7', '#f28e2b', '#e15759'])

    # Adiciona os valores acima das barras
    for bar, value in zip(bars, values):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{value:.1f}", ha='center', va='bottom', fontsize=10)

    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()

def plot_SIR_comparison(results: dict, path_dir: str = None):
    """
    Gera 4 gráficos comparando as curvas S, I, R e I_total entre múltiplos grafos.

    Args:
        results (dict): Dicionário com os nomes dos grafos como chave e um dict com listas 'S', 'I', 'R', 'I_total' como valor.
        path_dir (str, opcional): Diretório onde as imagens serão salvas. Se None, apenas exibe.
    """
    if path_dir:
        os.makedirs(path_dir, exist_ok=True)

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']  # até 6 grafos
    metrics = ['S', 'I', 'R', 'I_total']
    titles = {
        'S': "Comparação de Suscetíveis (S)",
        'I': "Comparação de Infectados (I)",
        'R': "Comparação de Recuperados (R)",
        'I_total': "Comparação de Infectados Totais",
    }

    for metric in metrics:
        plt.figure(figsize=(10, 6))

        for i, (nome, valores) in enumerate(results.items()):
            y = valores[metric]
            x = list(range(len(y)))
            plt.plot(x, y, label=nome, color=colors[i % len(colors)])

        plt.xlabel("Iterações")
        plt.ylabel(f"Número de {metric}")
        plt.title(titles[metric])
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if path_dir:
            caminho = os.path.join(path_dir, f"comparacao_{metric}.png")
            plt.savefig(caminho, dpi=300)
            plt.close()
        else:
            plt.show()

def plot_graph(
    G: nx.Graph,
    nome_arquivo: str = None,
    layout: str = "spring",  # apenas para grafos não georreferenciados
    figsize: tuple = (10, 8),
    node_size: int = 30,
    edge_color: str = "white",
    node_color: str = "skyblue",
    with_labels: bool = False
):
    """
    Plota um grafo, seja ele georreferenciado (OSMnx) ou abstrato (NetworkX).
    
    Args:
        G (nx.Graph): O grafo a ser plotado.
        nome_arquivo (str, opcional): Caminho para salvar o gráfico. Se None, apenas exibe.
        layout (str): Tipo de layout (apenas para grafos comuns). Ex: 'spring', 'circular', 'kamada_kawai'.
        figsize (tuple): Tamanho da figura.
        node_size (int): Tamanho dos nós.
        edge_color (str): Cor das arestas.
        node_color (str): Cor dos nós.
        with_labels (bool): Exibir rótulos nos nós.
    """
    is_geographic = 'x' in G.nodes[list(G.nodes)[0]] and 'y' in G.nodes[list(G.nodes)[0]]

    if is_geographic:
        # Grafo georreferenciado (OSMnx)
        fig, ax = ox.plot_graph(
            G,
            node_size=node_size,
            edge_color=edge_color,
            node_color=node_color,
            bgcolor="black",
            show=False,
            close=False,
            figsize=figsize
        )
        if nome_arquivo:
            fig.savefig(nome_arquivo, dpi=300)
            plt.close(fig)
        else:
            plt.show()

    else:
        # Grafo comum (sem coordenadas geográficas)
        # Escolhe o layout adequado
        if layout == "spring":
            pos = nx.spring_layout(G, seed=42, iterations=1)
        elif layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        elif layout == "spectral":
            pos = nx.spectral_layout(G)
        else:
            raise ValueError(f"Layout '{layout}' não é suportado.")

        plt.figure(figsize=figsize)
        nx.draw(
            G,
            pos,
            with_labels=with_labels,
            node_size=node_size,
            node_color=node_color,
            edge_color=edge_color,
            font_size=8
        )
        plt.title("Visualização do Grafo")
        plt.tight_layout()

        if nome_arquivo:
            plt.savefig(nome_arquivo, dpi=300)
            plt.close()
        else:
            plt.show()
            
def plot_graph_with_removed(
    G: nx.Graph,
    removed_nodes: list,
    nome_arquivo: str = None,
    layout: str = "spring",  # apenas para grafos não georreferenciados
    figsize: tuple = (10, 8),
    node_size: int = 30,
    edge_color: str = "white",
    node_color: str = "skyblue",
    removed_node_color: str = "red",
    with_labels: bool = False
):
    """
    Plota um grafo destacando visualmente os nós removidos.

    Args:
        G (nx.Graph): O grafo original.
        removed_nodes (list): Lista de nós removidos para destaque.
        nome_arquivo (str, opcional): Caminho para salvar o gráfico. Se None, apenas exibe.
        layout (str): Tipo de layout (para grafos comuns).
        figsize (tuple): Tamanho da figura.
        node_size (int): Tamanho dos nós.
        edge_color (str): Cor das arestas.
        node_color (str): Cor padrão dos nós.
        removed_node_color (str): Cor dos nós removidos.
        with_labels (bool): Exibir rótulos nos nós.
    """
    is_geographic = 'x' in G.nodes[list(G.nodes)[0]] and 'y' in G.nodes[list(G.nodes)[0]]

    if is_geographic:
        # Georreferenciado: precisamos separar os nós
        node_colors = []
        for node in G.nodes:
            if node in removed_nodes:
                node_colors.append(removed_node_color)
            else:
                node_colors.append(node_color)

        fig, ax = ox.plot_graph(
            G,
            node_size=node_size,
            edge_color=edge_color,
            node_color=node_colors,
            bgcolor="black",
            show=False,
            close=False,
            figsize=figsize
        )
        if nome_arquivo:
            fig.savefig(nome_arquivo, dpi=300)
            plt.close(fig)
        else:
            plt.show()

    else:
        # Grafo comum (abstrato)
        if layout == "spring":
            pos = nx.spring_layout(G, seed=42, iterations=10)
        elif layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        elif layout == "spectral":
            pos = nx.spectral_layout(G)
        else:
            raise ValueError(f"Layout '{layout}' não é suportado.")

        # Definir a cor de cada nó
        node_colors = []
        for node in G.nodes:
            if node in removed_nodes:
                node_colors.append(removed_node_color)
            else:
                node_colors.append(node_color)

        plt.figure(figsize=figsize)
        nx.draw(
            G,
            pos,
            with_labels=with_labels,
            node_size=node_size,
            node_color=node_colors,
            edge_color=edge_color,
            font_size=8
        )
        plt.title("Visualização do Grafo com Nós Removidos Destacados")
        plt.tight_layout()

        if nome_arquivo:
            plt.savefig(nome_arquivo, dpi=300)
            plt.close()
        else:
            plt.show()
