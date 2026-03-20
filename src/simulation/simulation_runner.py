class SimulationRunner:

    def __init__(self, population, strategies, environment):
        self.population = population
        self.strategies = strategies
        self.environment = environment

    def run(self, generations):

        for t in range(generations):

            self.population = self.strategies.mutation.mutate(self.population)

            fitness = self.strategies.selection.evaluate(
                self.population, self.environment
            )

            survivors = self.strategies.selection.select(
                self.population, fitness
            )

            self.population = self.strategies.reproduction.reproduce(
                survivors
            )

            self.environment.update()

            self.stats.record(self.population, self.environment)