import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from src.strategies.selection.selection_strategies import compute_fitnesses
from dataclasses import dataclass, field
from typing import List, Optional
import os


@dataclass
class AdvGenerationRecord:
    generation: int
    mean_fitness: float
    mean_phenotype: np.ndarray
    phenotype_variance: float
    distance_from_optimum: float
    population_size: int
    n_parents: int = 0
    median_offspring: float = 0.0
    max_offspring: int = 0
    n_clusters: int = 1
    cluster_sizes: list = field(default_factory=list)
    silhouette: float = np.nan
    extra: dict = field(default_factory=dict)


class AdvancedSimulationStats:
    def __init__(self, save_dir="data"):
        self.records = []
        self.extinct_at = None
        self.alpha_history = []

        self.save_dir = save_dir

        if self.save_dir is not None:
            os.makedirs(self.save_dir, exist_ok=True)

    def _find_best_clustering(self, phenotypes):
        """
        Finds optimal number of clusters using silhouette score.
        """
        n_samples = len(phenotypes)

        # jeśli za mało punktów → brak sensownego klastrowania
        if n_samples < 2:
            return 1, [n_samples], np.nan

        max_k = min(5, n_samples)  # ograniczenie dla stabilności

        best_k = 1
        best_score = -1
        best_labels = None

        for k in range(2, max_k + 1):
            try:
                kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
                labels = kmeans.fit_predict(phenotypes)

                # jeśli wszystko w jednym klastrze → pomiń
                if len(set(labels)) < 2:
                    continue

                score = silhouette_score(phenotypes, labels)

                if score > best_score:
                    best_score = score
                    best_k = k
                    best_labels = labels

            except Exception:
                continue

        # jeśli nic sensownego nie znaleziono
        if best_labels is None:
            return 1, [n_samples], np.nan

        cluster_sizes = [np.sum(best_labels == i) for i in range(best_k)]

        return best_k, cluster_sizes, best_score

    def record(self, generation, population, alpha, sigma, reproduction_strategy=None):
        individuals = population.get_individuals()
        if not individuals:
            return

        self.alpha_history.append(alpha.copy())

        phenotypes = np.array([ind.get_phenotype() for ind in individuals])
        fitnesses = compute_fitnesses(individuals, alpha, sigma)

        mean_phenotype = phenotypes.mean(axis=0)
        phenotype_variance = phenotypes.var(axis=0).mean()
        distance = float(np.linalg.norm(mean_phenotype - alpha))
        mean_fitness = float(fitnesses.mean())

        repro = (reproduction_strategy.get_reproduction_stats()
                 if reproduction_strategy else None) or {}

        # --- AUTOMATYCZNE KLASTROWANIE ---
        n_clusters, cluster_sizes, silhouette = self._find_best_clustering(phenotypes)

        self.records.append(AdvGenerationRecord(
            generation=generation,
            mean_fitness=mean_fitness,
            mean_phenotype=mean_phenotype,
            phenotype_variance=float(phenotype_variance),
            distance_from_optimum=distance,
            population_size=len(individuals),
            n_parents=repro.get('n_parents', 0),
            median_offspring=repro.get('median_offspring', 0.0),
            max_offspring=repro.get('max_offspring', 0),
            n_clusters=n_clusters,
            cluster_sizes=cluster_sizes,
            silhouette=silhouette,
        ))

    def mark_extinct(self, generation):
        self.extinct_at = generation

    def to_dataframe(self):
        df = pd.DataFrame([{
            'generation': r.generation,
            'mean_fitness': r.mean_fitness,
            'distance_from_optimum': r.distance_from_optimum,
            'phenotype_variance': r.phenotype_variance,
            'population_size': r.population_size,
            'n_parents': r.n_parents,
            'median_offspring': r.median_offspring,
            'max_offspring': r.max_offspring,
            'n_clusters': r.n_clusters,
            'silhouette': r.silhouette,
            'cluster_sizes': r.cluster_sizes,
        } for r in self.records])
        return df

    def save_csv(self, filename="simulation_stats.csv"):
        path = os.path.join(self.save_dir, filename)
        self.to_dataframe().to_csv(path, index=False)
        print(f"[INFO] Stats saved to {path}")

    def summary(self):
        if not self.records:
            return "Brak danych."
        last = self.records[-1]
        status = "Wymarła" if self.extinct_at is not None else "Przeżyła"
        return (
            f"Pokoleń: {last.generation + 1} | Status: {status}\n"
            f"Ostatnie śr. fitness: {last.mean_fitness:.4f} | "
            f"Odległość od optimum: {last.distance_from_optimum:.4f} | "
            f"Wariancja fenotypowa: {last.phenotype_variance:.4f} | "
            f"Liczba klastrów: {last.n_clusters} | "
            f"Silhouette: {last.silhouette:.4f}"
        )