import itertools
import numpy as np
import pandas as pd
import os

from src.simulation.simulation_runner import SimulationRunner
from src.core.population import Population
from src.strategies.environment.linear_environment import LinearShiftEnvironment
from src.strategies.mutation.isotropic_mutation import IsotropicMutation
from src.strategies.reproduction.reproduction import AsexualReproduction
from src.strategies.selection.selection_strategies import TwoStageSelection

# katalog
os.makedirs("data/raw/grid_search", exist_ok=True)

# --- zakresy parametrów ---
mu_values = [0.005, 0.01, 0.05]

xi_values = [0.001, 0.05, 0.1]

sigma_values = [0.2, 0.5, 1.0, 2.0]

c_values = [0.0, 0.002, 0.005, 0.01]  # więcej punktów dla środowiska

generations_values = [50, 100, 200]

results = []

for mu, xi, sigma, c_val, generations in itertools.product(
    mu_values, xi_values, sigma_values, c_values, generations_values
):
    print(f"[RUN] mu={mu}, xi={xi}, sigma={sigma}, c={c_val}, T={generations}")

    alpha_init = np.zeros(5)

    population = Population(
        size=100,
        n_dim=5,
        init_scale=0.1,
        alpha_init=alpha_init
    )

    environment = LinearShiftEnvironment(
        alpha_init=alpha_init,
        c=np.ones(5) * c_val,
        delta=0.0
    )

    mutation = IsotropicMutation(mu=mu, mu_c=0.1, xi=xi)
    selection = TwoStageSelection(sigma=sigma, threshold=0.2, N=100)
    reproduction = AsexualReproduction()

    runner = SimulationRunner(
        population=population,
        environment=environment,
        selection=selection,
        reproduction=reproduction,
        mutation=mutation,
        sigma=sigma,
        save_dir="data/raw/grid_search"
    )

    filename = f"run_mu{mu}_xi{xi}_sigma{sigma}_c{c_val}_T{generations}.csv"

    stats = runner.run(
        generations=generations,
        filename=filename
    )

    last = stats.records[-1] if stats.records else None

    results.append({
        "mu": mu,
        "xi": xi,
        "sigma": sigma,
        "c": c_val,
        "generations": generations,
        "extinct": stats.extinct_at is not None,
        "final_fitness": last.mean_fitness if last else np.nan,
        "final_variance": last.phenotype_variance if last else np.nan,
        "final_clusters": last.n_clusters if last else 0,
        "final_silhouette": last.silhouette if last else np.nan,
        "speciation": (
            last.n_clusters >= 2 and last.silhouette > 0.3
            if last else False
        )
    })

# zapis zbiorczy
df = pd.DataFrame(results)
df.to_csv("data/processed/grid_search_summary.csv", index=False)

print("[DONE] zapisano grid search")