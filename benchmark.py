import sys
import time
import threading
import os


from simulations.simulations_brandes import benchmark_brandes_custom
from plot.plot import plot_random_weights, plot_all_graph_brandes


class live_timer:
    def __init__(self, desc: str, interval: float = 0.2):
        self.desc = desc
        self.interval = interval
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        start = time.time()
        while not self._stop.is_set():
            elapsed = time.time() - start
            sys.stdout.write(f"\r{self.desc}: {elapsed:5.1f}s")
            sys.stdout.flush()
            time.sleep(self.interval)
        elapsed = time.time() - start
        sys.stdout.write(f"\r{self.desc} → concluído em {elapsed:.2f}s\n")
        sys.stdout.flush()

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop.set()
        self._thread.join()


def main():
    os.makedirs('imgs/brandes', exist_ok=True)

    graph_sizes = [50, 100, 200, 300, 400, 500, 1000, 1500, 2000, 3000]
    num_repeats = 3
    seed = 42
    folder = 'imgs/brandes'
    tipos_grafo = ['erdos', 'planar']

    resultados_todos = {}

    with live_timer("Benchmark completo"):
        for tipo in tipos_grafo:
            print(f"\n>>> Benchmark: {tipo.upper()}")
            resultados = benchmark_brandes_custom(
                sizes=graph_sizes,
                graph_type=tipo,
                num_repeats=num_repeats,
                seed=seed,
                folder=folder,
                save_img=True  # Salva imagens dos grafos base
            )
            resultados_todos[tipo] = resultados

            # Gráfico individual de cada tipo
            nome_grafico = f'{folder}/brandes_{tipo}_normalizado.png'
            print(f" → Gerando gráfico individual: {nome_grafico}")
            plot_random_weights(
                resultados['sizes'],
                resultados['random_weights'],
                label=f'{tipo.capitalize()} (Pesos Aleatórios)',
                save_path=nome_grafico
            )

    # Gráfico comparativo final
    print("\n>>> Gerando gráfico comparativo com todos os tipos de grafo...")
    plot_all_graph_brandes(
        resultados_por_tipo=resultados_todos,
        save_path=f'{folder}/brandes_comparativo_todos.png'
    )
    print(" → Comparação salva em 'imgs/brandes/brandes_comparativo_todos.png'\n")

if __name__ == "__main__":
    main()
