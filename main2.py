import sys
import time
import threading
import os


from simulations.simulations_brandes import benchmark_brandes_custom
from plot.plot import plot_random_weights


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
    # Cria pasta imgs/brandes se não existir
    folder = 'imgs/brandes'
    os.makedirs(folder, exist_ok=True)

    # Configurações do experimento
    graph_sizes = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900,
               1000, 1250, 1500, 2000, 3000, 4000, 5000]
    graph_type = 'barabasi'
    num_repeats = 5
    seed = 42

    print(f"\nBenchmark de Brandes usando grafos {graph_type}...\n")

    with live_timer("Benchmark completo"):
        results = benchmark_brandes_custom(
            sizes=graph_sizes,
            graph_type=graph_type,
            num_repeats=num_repeats,
            seed=seed,
            folder=folder
        )

    # Geração do gráfico
    print("\nGerando gráfico de tempos normalizados (somente pesos aleatórios)...")
    plot_random_weights(
        graph_sizes,
        results['random_weights'],
        label='Pesos Aleatórios',
        save_path='imgs/brandes/brandes_comparacao_normalizada.png'
    )
    print(" → Gráfico salvo em 'imgs/brandes/brandes_comparacao_normalizada.png'\n")

if __name__ == "__main__":
    main()
