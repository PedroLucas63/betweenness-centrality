import lib.graph_lib as glib
import random
from tqdm import tqdm
from utils.utils import clip

def simulate_SI(graph: glib.Graph, steps: int=20, beta: float=0.3, verbose: bool=False):
    """
    Simulação de pandemia estilo SI (Susceptible-Infected).
    
    Args:
        graph (glib.Graph): Grafo do graph_lib
        steps (int): Número de iterações da simulação
        beta (float): Taxa de transmissão
        verbose (bool): Se True, mostra a barra de progresso
    
    Returns:
        list: Contagem de infectados em cada iteração
    """
    nodes = graph.nodes()
    if not nodes:
        return []

    infected = set([random.choice(nodes)])  # Começa com 1 infectado aleatório
    infected_count = [len(infected)]
    
    progress = tqdm(range(1, steps+1), desc="Simulação de Pandemia - Evolução da Infecção", disable=not verbose)
    
    for step in progress:
        novos_infectados = set()
        for u in infected:
            for v in graph[u]:
                if v not in infected:
                    if random.random() < beta:
                        novos_infectados.add(v)

        infected.update(novos_infectados)
        infected_count.append(len(infected))

        progress.set_description(f"Iteração {step} -> S: {len(nodes) - len(infected)}, I: {len(infected)}")
        
        if len(infected) == graph.size():
            break

    return infected_count

def simulate_SIR(graph: glib.Graph, beta: float=0.3, gamma: float=0.1, steps: int=50, verbose: bool=False):
    """
    Simulação SIR (Suscetíveis-Infectados-Recuperados) sobre um grafo.
    
    Args:
        graph (glib.Graph): Grafo do graph_lib
        beta (float): Taxa de transmissão
        gamma (float): Taxa de recuperação
        steps (int): Número de iterações da simulação
        verbose (bool): Se True, mostra a barra de progresso
    
    Returns:
        list: Contagem de suscetíveis, infectados e recuperados em cada iteração
    """
    nodes = graph.nodes()
    if not nodes:
        return []
    
    status = {node: 'S' for node in nodes}

    # Começa com 0.1% dos nó infectado aleatório
    k = max(1, int(len(nodes) * 0.001))
    infected = random.sample(nodes, k)
    
    for node in infected:
        status[node] = 'I'

    S_count = [len(nodes) - k]
    I_count = [k]
    R_count = [0]
    
    progress = tqdm(range(1, steps+1), desc="Simulação de Pandemia - Evolução da Infecção", disable=not verbose)

    for step in progress:
        new_status = status.copy()

        for node in nodes:
            if status[node] == 'I':
                for neighbor in graph[node]:
                    weight = graph[node][neighbor]['weight']
                    x = -0.0001189*weight**2 + 0.0002378*weight + 0.29988
                    prob = clip(x, 0.1, beta)
                    
                    if status[neighbor] == 'S' and random.random() < prob:
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

        progress.set_description(f"Iteração {step} -> S: {S}, I: {I}, R: {R}")

        # Encerra se não houver mais suscetíveis
        if S == 0:
            break

    return S_count, I_count, R_count