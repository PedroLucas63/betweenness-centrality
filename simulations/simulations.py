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

def simulate_SIR(graph: glib.Graph,
                 beta: float = 0.3,
                 gamma: float = 0.1,
                 steps: int = 50,
                 mean_weight: float = 1,
                 verbose: bool = False,
                 min_days_infected: int = 3,
                 days_to_lose_immunity: int = None):
    """
    Simulação SIR com suporte a tempo mínimo de infecção e perda de imunidade.

    Args:
        graph (glib.Graph): Grafo do graph_lib
        beta (float): Taxa de transmissão
        gamma (float): Taxa de recuperação
        steps (int): Número de iterações
        mean_weight (float): Peso médio das arestas
        verbose (bool): Se True, exibe barra de progresso
        min_days_infected (int): Dias mínimos para recuperação
        days_to_lose_immunity (int): Dias para um recuperado voltar a ser suscetível

    Returns:
        tuple: Listas S, I, R ao longo das iterações
    """
    nodes = graph.nodes()
    if not nodes:
        return []

    status = {node: 'S' for node in nodes}
    days_infected = {}
    days_recovered = {}

    k = max(1, int(len(nodes) * 0.001))
    infected = random.sample(nodes, k)
    for node in infected:
        status[node] = 'I'
        days_infected[node] = 0

    S_count = [len(nodes) - k]
    I_count = [k]
    R_count = [0]

    progress = tqdm(range(1, steps + 1),
                    desc="Simulação de Pandemia - Evolução da Infecção",
                    disable=not verbose)

    for step in progress:
        new_status = status.copy()
        new_days_infected = days_infected.copy()
        new_days_recovered = days_recovered.copy()

        for node in nodes:
            if status[node] == 'I':
                # Tenta infectar vizinhos
                for neighbor in graph[node]:
                    weight = graph[node][neighbor]['weight']
                    prob = clip(beta * (mean_weight / weight), 0.075, beta)
                    if status[neighbor] == 'S' and random.random() < prob:
                        new_status[neighbor] = 'I'
                        new_days_infected[neighbor] = 0

                # Atualiza tempo infectado
                new_days_infected[node] += 1

                # Só pode se recuperar após X dias
                if new_days_infected[node] >= min_days_infected and random.random() < gamma:
                    new_status[node] = 'R'
                    del new_days_infected[node]
                    new_days_recovered[node] = 0

            elif status[node] == 'R':
                # Atualiza tempo como recuperado
                if days_to_lose_immunity is not None:
                    new_days_recovered[node] += 1
                    if new_days_recovered[node] >= days_to_lose_immunity:
                        new_status[node] = 'S'
                        del new_days_recovered[node]

        status = new_status
        days_infected = new_days_infected
        days_recovered = new_days_recovered

        S = sum(1 for s in status.values() if s == 'S')
        I = sum(1 for s in status.values() if s == 'I')
        R = sum(1 for s in status.values() if s == 'R')

        S_count.append(S)
        I_count.append(I)
        R_count.append(R)

        progress.set_description(f"Iteração {step} -> S: {S}, I: {I}, R: {R}")

        if S == 0 and I == 0:
            break

    return S_count, I_count, R_count
