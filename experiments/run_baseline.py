import numpy as np
import pickle
import os
from datetime import datetime

from src.core.population import Population
from src.strategies.environment.linear_environment import LinearShiftEnvironment
from src.strategies.mutation.isotropic_mutation import IsotropicMutation
from src.strategies.selection.selection_strategies import TwoStageSelection
from src.strategies.reproduction.reproduction import AsexualReproduction
from src.simulation.simulation_runner import SimulationRunner


# =========================
# Experiment configuration
# =========================

N_REPLICATES = 20
GENERATIONS = 75

N_DIM = 5
POP_SIZE = 100

SIGMA = 0.5
MU = 0.005
MU_C = 0.1
XI = 0.05

THRESHOLD = 0.2
C_VALUES = {
    "baseline": 0.0,
    "extension": 0.005
}

OUTPUT_PATH = "data/experiment_results.pkl"

# Optional: separate seeds explicitly
SEEDS = list(range(N_REPLICATES))


# =========================
# Storage structure
# =========================

results = {
    "metadata": {
        "created_at": datetime.now().isoformat(),
        "generations": GENERATIONS,
        "n_replicates": N_REPLICATES,
        "n_dim": N_DIM,
        "pop_size": POP_SIZE,
        "sigma": SIGMA,
        "mu": MU,
        "mu_c": MU_C,
        "xi": XI,
        "threshold": THRESHOLD,
        "c_values": C_VALUES
    },
    "runs": {}
}


# =========================
# Run experiment
# =========================

for condition_name, c_val in C_VALUES.items():
    print(f"\n=== Running condition: {condition_name} (c={c_val}) ===")

    results["runs"][condition_name] = []

    for seed in SEEDS:
        print(f"  -> Seed {seed}")

        # Reproducibility
        np.random.seed(seed)

        # Initial phenotype
        alpha_init = np.zeros(N_DIM)

        # Population
        population = Population(
            size=POP_SIZE,
            n_dim=N_DIM,
            init_scale=0.1,
            alpha_init=alpha_init
        )

        # Environment (linear drift)
        environment = LinearShiftEnvironment(
            alpha_init=alpha_init,
            c=np.ones(N_DIM) * c_val,
            delta=0.0
        )

        # Evolutionary operators
        mutation = IsotropicMutation(mu=MU, mu_c=MU_C, xi=XI)
        selection = TwoStageSelection(
            sigma=SIGMA,
            threshold=THRESHOLD,
            N=POP_SIZE
        )
        reproduction = AsexualReproduction()

        # Simulation runner
        runner = SimulationRunner(
            population=population,
            environment=environment,
            selection=selection,
            reproduction=reproduction,
            mutation=mutation,
            sigma=SIGMA,
            save_dir=None   
        )

        # Run simulation
        stats = runner.run(generations=GENERATIONS)

        # Store result with seed info
        results["runs"][condition_name].append({
            "seed": seed,
            "stats": stats.to_dataframe().to_dict(orient="list"),
            "extinct_at": stats.extinct_at
        })


# =========================
# Save results
# =========================

os.makedirs("data", exist_ok=True)

with open(OUTPUT_PATH, "wb") as f:
    pickle.dump(results, f)

print(f"\nResults saved to {OUTPUT_PATH}")