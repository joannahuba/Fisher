# reproduction.py

import copy
import numpy as np
from strategies import ReproductionStrategy


class AsexualReproduction(ReproductionStrategy):
    """
    Reprodukcja bezpłciowa (klonowanie):
    Losowo wybiera rodziców spośród ocalałych (z powtórzeniami) i klonuje ich,
    aby uzyskać dokładnie target_size osobników nowego pokolenia.

    Każdy ocalały ma równe szanse na bycie rodzicem – selekcja już uwzględniła fitness.
    Po każdym wywołaniu reproduce() dostępne są statystyki przez get_reproduction_stats().
    """

    def __init__(self):
        self._last_counts: np.ndarray = np.array([])

    def reproduce(self, survivors: list, target_size: int) -> list:
        if not survivors:
            self._last_counts = np.array([])
            return []
        indices = np.random.randint(0, len(survivors), size=target_size)
        # bincount[i] = liczba potomków osobnika i
        self._last_counts = np.bincount(indices, minlength=len(survivors))
        return [copy.deepcopy(survivors[i]) for i in indices]

    def get_reproduction_stats(self) -> dict:
        """
        Zwraca statystyki z ostatniego reproduce():
          n_parents       – ilu osobników miało ≥1 potomka ("ewolucyjny sukces")
          median_offspring – mediana potomków wśród reprodukujących się osobników
          max_offspring   – maksymalna płodność (najlepiej przystosowany osobnik)
        """
        if len(self._last_counts) == 0:
            return {'n_parents': 0, 'median_offspring': 0.0, 'max_offspring': 0}
        reproducing = self._last_counts[self._last_counts > 0]
        return {
            'n_parents':        int(len(reproducing)),
            'median_offspring': float(np.median(reproducing)) if len(reproducing) else 0.0,
            'max_offspring':    int(self._last_counts.max()),
        }


# Funkcja pomocnicza zachowana dla kompatybilności wstecznej
def asexual_reproduction(survivors: list, N: int) -> list:
    return AsexualReproduction().reproduce(survivors, N)

class SexualReproduction(ReproductionStrategy):
    """
    Reprodukcja płciowa:
    - losowo wybiera pary rodziców z listy ocalałych
    - dzieci mają cechy będące średnią cech rodziców
    - liczba dzieci = target_size
    - brak ograniczenia ile razy ktoś moze być rodzicem
    """

    def __init__(self,sigma_mutation):
        self._last_counts: np.ndarray = np.array([])
        self.sigma_mutation=sigma_mutation

    def reproduce(self, survivors: list, target_size: int) -> list:
        if not survivors:
            self._last_counts=np.array([])
            return []

        N = len(survivors)
        children = []
        counts=np.zeros(N, dtype=int)

        for _ in range(target_size):
            # Wybór losowej pary rodziców
            i1,i2=np.random.randint(0,N,size=2)
            parent1, parent2=survivors[i1],survivors[i2]

            # Crossover: średnia cech dwóch rodziców
            child=copy.deepcopy(parent1)
            child_pheno = (parent1.get_phenotype() + parent2.get_phenotype()) / 2
            child_pheno += np.random.normal(0, self.sigma_mutation, size=child_pheno.shape)
            child.set_phenotype(child_pheno)

            children.append(child)
            counts[i1] +=1
            counts[i2] +=1

        
        self._last_counts=counts
        return children
        
    def get_reproduction_stats(self) -> dict:
        if len(self._last_counts) == 0:
            return {'n_parents': 0, 'median_offspring': 0.0, 'max_offspring': 0}
        reproducing = self._last_counts[self._last_counts > 0]
        return {
            'n_parents':        int(len(reproducing)),
            'median_offspring': float(np.median(reproducing)) if len(reproducing) else 0.0,
            'max_offspring':    int(self._last_counts.max()),
        }

'''
def sexual_reproduction(survivors: list, N: int) -> list:
    return SexualReproduction().reproduce(survivors, N)
'''

