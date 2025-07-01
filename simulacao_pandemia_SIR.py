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

def simular_SIR(graph, beta=0.3, gamma=0.1, steps=50, print_steps=True):
    """
    Simulação SIR (Suscetíveis-Infectados-Recuperados) sobre um grafo.
    """
    nodes = graph.nodes()
    status = {node: 'S' for node in nodes}

    # Começa com um nó infectado aleatório
    initial_infected = random.choice(nodes)
    status[initial_infected] = 'I'

    S_count = [len(nodes) - 1]
    I_count = [1]
    R_count = [0]

    if print_steps:
        print(f"Iteração 0 -> S: {S_count[0]}, I: {I_count[0]}, R: {R_count[0]}")

    for step in range(1, steps+1):
        new_status = status.copy()

        for node in nodes:
            if status[node] == 'I':
                for neighbor in graph[node]:
                    if status[neighbor] == 'S' and random.random() < beta:
                        new_status[neighbor] = 'I'

                if random.random() < gamma:
                    new_status[node] = 'R'

        status = new_status

        S = sum(1 for s in status.values() if s == 'S')
        I = sum(1 for s in status.values() if s == 'I')
        R = sum(1 for s in status.values() if s == 'R')

        S_count.append(S)
        I_count.append(I)
        R_count.append(R)

        if print_steps:
            print(f"Iteração {step} -> S: {S}, I: {I}, R: {R}")

        # Encerra se não houver mais infectados
        if I == 0:
            print(f"Fim da pandemia na iteração {step}.\n")
            break

    return S_count, I_count, R_count

def plot_SIR_comparativo(S_before, I_before, R_before, S_after, I_after, R_after):
    plt.figure(figsize=(10,6))

    plt.plot(I_before, label='Infectados - Antes (rede completa)', color='red', linestyle='-')
    plt.plot(I_after, label='Infectados - Depois (hubs removidos)', color='purple', linestyle='--')

    plt.xlabel('Iterações')
    plt.ylabel('Número de Infectados')
    plt.title('Comparação da Infecção - Antes vs Depois da Remoção de Hubs')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # plt.savefig('comparativo_sir.png', dpi=300)

if __name__ == '__main__':
    print("=== Carregando grafo da cidade ===")
    G_natal = load_natal_graph()
    print(f"Tamanho inicial da rede: {G_natal.size()} nós.\n")

    print("=== Calculando centralidade de intermediação (Brandes) ===")
    centralidade = glib.brandes(G_natal)

    print("\n=== Simulando SIR antes da remoção de hubs ===")
    start_time = time.time()
    S_before, I_before, R_before = simular_SIR(G_natal, beta=0.3, gamma=0.1, steps=50)
    print(f"Tempo de simulação (antes): {time.time() - start_time:.2f} segundos\n")

    print("=== Removendo top 10% dos nós mais centrais ===")
    remove_top_10_percent(G_natal, centralidade)

    print("\n=== Simulando SIR depois da intervenção ===")
    start_time = time.time()
    S_after, I_after, R_after = simular_SIR(G_natal, beta=0.3, gamma=0.1, steps=50)
    print(f"Tempo de simulação (depois): {time.time() - start_time:.2f} segundos\n")

    print("=== Exibindo gráfico comparativo (Infectados) ===")
    plot_SIR_comparativo(S_before, I_before, R_before, S_after, I_after, R_after)
