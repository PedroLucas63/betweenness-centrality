from cidade_graph import load_natal_graph
import graph_lib as glib
import random
import matplotlib.pyplot as plt
import time

def remove_top_10_percent(graph, centralidade):
    num_to_remove = max(1, int(0.1 * graph.size()))
    top_nodes = sorted(centralidade.items(), key=lambda x: x[1], reverse=True)[:num_to_remove]
    print(f"\nNúmero de nós a remover: {num_to_remove}")

    for node, _ in top_nodes:
        graph._adjacency_list.pop(node, None)
        for neighbors in graph._adjacency_list.values():
            neighbors.pop(node, None)

    print(f"Após remoção: tamanho da rede = {graph.size()} nós.")

def simular_SI(graph, steps=20):
    """
    Simulação de pandemia estilo SI (Susceptible-Infected).
    """
    nodes = graph.nodes()
    if not nodes:
        print("Grafo vazio! Não é possível simular.")
        return []

    infected = set([random.choice(nodes)])  # Começa com 1 infectado aleatório
    infected_count = [len(infected)]

    print(f"\nInício da simulação SI:")
    print(f"Nó inicial infectado: {list(infected)[0]}")

    for step in range(steps):
        novos_infectados = set()
        for u in infected:
            for v in graph[u]:
                if v not in infected:
                    if random.random() < 0.3:  # Probabilidade de infecção 30%
                        novos_infectados.add(v)

        infected.update(novos_infectados)
        infected_count.append(len(infected))

        print(f"Iteração {step+1}: {len(novos_infectados)} novos infectados, total = {len(infected)}")

        if len(infected) == graph.size():
            print(">>> Todos os nós foram infectados! Encerrando simulação.\n")
            break

    return infected_count

def plot_resultado(original, modificado):
    plt.figure(figsize=(8,6))
    plt.plot(original, label="Antes (rede completa)", color='blue', marker='o')
    plt.plot(modificado, label="Depois (hubs removidos)", color='red', marker='x')
    plt.xlabel("Iterações")
    plt.ylabel("Número de infectados")
    plt.title("Simulação de Pandemia - Evolução da Infecção")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    print("=== Carregando grafo da cidade ===")
    G_natal = load_natal_graph()
    print(f"Tamanho inicial da rede: {G_natal.size()} nós.\n")

    print("=== Calculando centralidade de intermediação (Brandes) ===")
    centralidade = glib.brandes(G_natal)

    print("=== Simulando pandemia antes de remover hubs ===")
    start_time = time.time()
    resultado_original = simular_SI(G_natal, steps=20)
    duration = time.time() - start_time
    print(f"Tempo de simulação (antes da remoção): {duration:.2f} segundos\n")

    print("=== Removendo top 10% dos nós mais centrais ===")
    remove_top_10_percent(G_natal, centralidade)

    print("=== Simulando pandemia depois da intervenção ===")
    start_time = time.time()
    resultado_modificado = simular_SI(G_natal, steps=20)
    duration = time.time() - start_time
    print(f"Tempo de simulação (após a remoção): {duration:.2f} segundos\n")

    print("=== Exibindo gráfico comparativo ===")
    plot_resultado(resultado_original, resultado_modificado)
