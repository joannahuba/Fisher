from src.core.population import Population
from src.strategies.selection.selection_strategies import compute_fitnesses
from src.simulation.stats import AdvancedSimulationStats  # <-- nowa klasa

class SimulationRunner:
    def __init__(self, population: Population, environment, 
                 selection, reproduction, mutation, sigma=1.0,
                 save_dir=None):   # 👈 ZMIANA

        self.population = population
        self.environment = environment
        self.selection = selection
        self.reproduction = reproduction
        self.mutation = mutation
        self.sigma = sigma

        self.stats = AdvancedSimulationStats(
            save_dir=save_dir   # None = brak ciężkiego IO
        )

    def run(self, generations: int, filename="simulation_stats.csv"):
        for generation in range(generations):
            alpha = self.environment.get_optimal_phenotype()

            # 1. Mutacja
            self.mutation.mutate(self.population)

            # 2. Selekcja
            survivors = self.selection.select(
                self.population.get_individuals(),
                alpha
            )

            if not survivors:
                self.stats.mark_extinct(generation)
                print(f"[INFO] Populacja wymarła w pokoleniu {generation}")
                break

            # 3. Reprodukcja
            new_individuals = self.reproduction.reproduce(
                survivors,
                len(self.population)
            )
            self.population.set_individuals(new_individuals)

            # 4. Statystyki
            self.stats.record(
                generation,
                self.population,
                alpha,
                self.sigma,
                reproduction_strategy=self.reproduction
            )

            # 5. Środowisko
            self.environment.update()

        # CSV opcjonalnie (lekki i przydatny)
        if self.stats.save_dir is not None:
            self.stats.save_csv(filename=filename)

        return self.stats