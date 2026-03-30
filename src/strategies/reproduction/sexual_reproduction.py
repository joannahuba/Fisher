import numpy as np
import copy
from src.strategies.strategies import ReproductionStrategy


class SexualReproduction(ReproductionStrategy):
    """
    Reprodukcja płciowa:
    - wybór dwóch rodziców
    - dziecko = średnia fenotypów + mała mutacja
    """

    def __init__(self, sigma_mutation: float = 0.01):
        self.sigma_mutation = sigma_mutation

    def reproduce(self, survivors, target_size):
        if not survivors:
            return []

        children = []
        N = len(survivors)

        for _ in range(target_size):
            i1, i2 = np.random.randint(0, N, size=2)
            parent1 = survivors[i1]
            parent2 = survivors[i2]

            p1 = parent1.get_phenotype()
            p2 = parent2.get_phenotype()

            child_pheno = (p1 + p2) / 2
            child_pheno += np.random.normal(0, self.sigma_mutation, size=child_pheno.shape)

            child = copy.deepcopy(parent1)
            child.set_phenotype(child_pheno)

            children.append(child)

        return children