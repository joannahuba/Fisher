class ShockEnvironment(EnvironmentDynamics):

    def __init__(self, alpha_init, c, T_shock, sigma_shock):

        self.alpha = alpha_init
        self.c = c
        self.T_shock = T_shock
        self.sigma_shock = sigma_shock
        self.generation = 0

    def update(self):

        self.alpha = self.alpha + self.c

        if self.generation % self.T_shock == 0:

            shock = np.random.normal(0, self.sigma_shock, size=len(self.alpha))

            self.alpha = self.alpha + shock

        self.generation += 1