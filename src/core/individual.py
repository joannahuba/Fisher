# individual.py

import numpy as np

class Individual:
    def __init__(self, phenotype: np.ndarray):
        self.phenotype = phenotype.copy()

    def get_phenotype(self) -> np.ndarray:
        return self.phenotype

    def set_phenotype(self, new_phenotype: np.ndarray):
        self.phenotype = new_phenotype.copy()
