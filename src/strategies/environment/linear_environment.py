# environment.py

import numpy as np
from src.strategies.strategies import EnvironmentDynamics

class LinearShiftEnvironment(EnvironmentDynamics):
    """
    Scenariusz globalnego ocieplenia: optymalny fenotyp przesuwa się liniowo
    z opcjonalnymi losowymi fluktuacjami w każdym pokoleniu.

        alpha(t) = alpha(t-1) + N(c, delta^2 * I)

    Jeśli delta=0, przesunięcie jest czysto deterministyczne:
        alpha(t) = alpha(t-1) + c
    """

    def __init__(self, alpha_init: np.ndarray, c: np.ndarray, delta: float = 0.0):
        """
        :param alpha_init: początkowy optymalny fenotyp
        :param c: wektor kierunkowej zmiany (średnie przesunięcie na pokolenie)
        :param delta: odch. std. losowych fluktuacji wokół c (0 = brak szumu)
        """
        self.alpha = np.array(alpha_init, dtype=float)
        self.c = np.array(c, dtype=float)
        self.delta = float(delta)

    def update(self) -> None:
        """alpha(t) = alpha(t-1) + N(c, delta^2 * I)"""
        if self.delta > 0:
            shift = np.random.normal(loc=self.c, scale=self.delta, size=len(self.alpha))
        else:
            shift = self.c.copy()
        self.alpha = self.alpha + shift

    def get_optimal_phenotype(self) -> np.ndarray:
        return self.alpha.copy()


# Alias dla kompatybilności wstecznej
Environment = LinearShiftEnvironment

class DualOptimumEnvironment(EnvironmentDynamics):
    def __init__(self, alpha1: np.ndarray, alpha2: np.ndarray, c1: np.ndarray, c2: np.ndarray, 
                 delta: float=0.0, jump_every: int = 0, jump_scale: float = 0.1):
        
        """
        :param jump_every: co ile pokoleń robimy nagły „skok” optima (0 = brak skoków)
        :param jump_scale: standardowe odchylenie dla skoku
        """
        
        self.alpha1=np.array(alpha1, dtype=float)
        self.alpha2=np.array(alpha2,dtype=float)
        self.c1 = np.array(c1, dtype=float)
        self.c2 = np.array(c2, dtype=float)
        self.delta = float(delta)
        self.jump_every=jump_every
        self.jump_scale=jump_scale
        self.generation=0
    
    def update(self) -> None:
        def step(alpha,c):
            if self.delta > 0:
                shift=np.random.normal(loc=c,scale=self.delta,size=len(alpha))
            else:
                shift=c.copy()
            return alpha + shift
        
        # standardowa zmiana środowiska
        self.alpha1=step(self.alpha1,self.c1)
        self.alpha2=step(self.alpha2,self.c2)

        # skokowe zmiany co jump_every pokoleń
        if self.jump_every > 0 and self.generation % self.jump_every == 0:
            self.alpha1 += np.random.normal(0, self.jump_scale, size=len(self.alpha1))
            self.alpha2 += np.random.normal(0, self.jump_scale, size=len(self.alpha2))
        
        self.generation +=1 
    
    def get_optimal_phenotype(self):
        return [self.alpha1.copy(), self.alpha2.copy()]

