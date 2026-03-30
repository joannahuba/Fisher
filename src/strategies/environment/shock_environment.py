from src.strategies.strategies import EnvironmentDynamics
import numpy as np

class ShockEnvironment(EnvironmentDynamics):
    def __init__(self, alpha_init, c, T_shock, sigma_shock):
        self.alpha = np.array(alpha_init, dtype=float)
        self.c = np.array(c, dtype=float)
        self.T_shock = T_shock
        self.sigma_shock = sigma_shock
        self.generation = 0

    def update(self):
        self.alpha = self.alpha + self.c

        if self.generation % self.T_shock == 0:
            shock = np.random.normal(0, self.sigma_shock, size=len(self.alpha))
            self.alpha = self.alpha + shock

        self.generation += 1

    def get_optimal_phenotype(self):
        return self.alpha.copy()