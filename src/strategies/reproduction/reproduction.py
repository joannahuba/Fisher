import copy
import numpy as np
from src.strategies.strategies import ReproductionStrategy


class AsexualReproduction(ReproductionStrategy):
    def __init__(self):
        self._last_counts: np.ndarray = np.array([])

    def reproduce(self, survivors: list, target_size: int) -> list:
        if not survivors:
            self._last_counts = np.array([])
            return []

        indices = np.random.randint(0, len(survivors), size=target_size)
        self._last_counts = np.bincount(indices, minlength=len(survivors))

        return [copy.deepcopy(survivors[i]) for i in indices]

    def get_reproduction_stats(self) -> dict:
        if len(self._last_counts) == 0:
            return {'n_parents': 0, 'median_offspring': 0.0, 'max_offspring': 0}

        reproducing = self._last_counts[self._last_counts > 0]

        return {
            'n_parents': int(len(reproducing)),
            'median_offspring': float(np.median(reproducing)) if len(reproducing) else 0.0,
            'max_offspring': int(self._last_counts.max()),
        }


def asexual_reproduction(survivors: list, N: int) -> list:
    return AsexualReproduction().reproduce(survivors, N)