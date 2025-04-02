import numpy as np
import random
import matplotlib.pyplot as plt
from time import time


class GeneticTSP:
    def __init__(
        self,
        cities,
        population_size=100,
        elite_size=20,
        mutation_rate=0.01,
        generations=500,
    ):
        self.cities = cities
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.distance_matrix = self._calculate_distance_matrix()

    def _calculate_distance_matrix(self):
        num_cities = len(self.cities)
        matrix = np.zeros((num_cities, num_cities))

        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                dist = np.sqrt(
                    (self.cities[i][0] - self.cities[j][0]) ** 2
                    + (self.cities[i][1] - self.cities[j][1]) ** 2
                )
                matrix[i][j] = dist
                matrix[j][i] = dist

        return matrix

    def _create_initial_population(self):
        population = []
        for _ in range(self.population_size):

            route = list(range(len(self.cities)))
            random.shuffle(route)
            population.append(route)
        return population

    def _calculate_route_distance(self, route):
        total_distance = 0
        for i in range(len(route)):
            from_city = route[i]
            to_city = route[(i + 1) % len(route)]
            total_distance += self.distance_matrix[from_city][to_city]
        return total_distance

    def _calculate_fitness(self, route):
        distance = self._calculate_route_distance(route)
        return 1 / distance

    def _rank_routes(self, population):
        fitness_results = {}
        for i, route in enumerate(population):
            fitness_results[i] = self._calculate_fitness(route)
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)

    def _selection(self, ranked_population):
        selection_results = []

        for i in range(self.elite_size):
            selection_results.append(ranked_population[i][0])

        fitness_sum = sum(
            [ranked_population[i][1] for i in range(len(ranked_population))]
        )
        for _ in range(self.population_size - self.elite_size):
            pick = random.random() * fitness_sum
            current_sum = 0
            for i in range(len(ranked_population)):
                current_sum += ranked_population[i][1]
                if current_sum >= pick:
                    selection_results.append(ranked_population[i][0])
                    break

        return selection_results

    def _create_mating_pool(self, population, selection_results):
        mating_pool = []
        for i in selection_results:
            mating_pool.append(population[i])
        return mating_pool

    def _ordered_crossover(self, parent1, parent2):
        child = [-1] * len(parent1)

        start, end = sorted(random.sample(range(len(parent1)), 2))

        for i in range(start, end + 1):
            child[i] = parent1[i]

        parent2_idx = 0
        for i in range(len(child)):
            if child[i] == -1:
                while parent2[parent2_idx] in child:
                    parent2_idx += 1
                child[i] = parent2[parent2_idx]
                parent2_idx += 1

        return child

    def _breed_population(self, mating_pool):
        children = []

        for i in range(self.elite_size):
            children.append(mating_pool[i])

        for i in range(self.population_size - self.elite_size):
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            child = self._ordered_crossover(parent1, parent2)
            children.append(child)

        return children

    def _mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(individual) - 1)
                individual[i], individual[j] = individual[j], individual[i]
        return individual

    def _mutate_population(self, population):
        mutated_pop = []

        for i in range(self.elite_size):
            mutated_pop.append(population[i])

        for i in range(self.elite_size, self.population_size):
            mutated_individual = self._mutate(population[i])
            mutated_pop.append(mutated_individual)

        return mutated_pop

    def run(self):
        population = self._create_initial_population()

        progress = []
        best_route = None
        best_distance = float("inf")

        start_time = time()

        for generation in range(self.generations):
            ranked_population = self._rank_routes(population)

            current_best_route = population[ranked_population[0][0]]
            current_best_distance = self._calculate_route_distance(current_best_route)
            progress.append(current_best_distance)

            if current_best_distance < best_distance:
                best_distance = current_best_distance
                best_route = current_best_route

            selection_results = self._selection(ranked_population)
            mating_pool = self._create_mating_pool(population, selection_results)

            children = self._breed_population(mating_pool)
            population = self._mutate_population(children)

        end_time = time()

        return {
            "progress": progress,
            "best_route": best_route,
            "best_distance": best_distance,
            "time": end_time - start_time,
        }


def main():
    np.random.seed(42)
    cities = [(np.random.randint(0, 200), np.random.randint(0, 200)) for _ in range(10)]

    print("Cities:")
    for i, (x, y) in enumerate(cities):
        print(f"City {i}: ({x}, {y})")

    ga = GeneticTSP(cities)
    results = ga.run()

    print("\nProgress:")
    for i in range(0, len(results["progress"]), 25):
        print(f"Generation {i}:", results["progress"][i])

    print("\nResults:")
    print(f"Best route: {results['best_route']}")
    print(f"Best distance: {results['best_distance']:.2f}")
    print(f"Execution time: {results['time']:.2f} seconds")

    print("\nRoute in order:")
    for i, city_idx in enumerate(results["best_route"]):
        print(f"{i+1}. City {city_idx}: {cities[city_idx]}")
    print(
        f"{len(results['best_route'])+1}. Return to City {results['best_route'][0]}: {cities[results['best_route'][0]]}"
    )


if __name__ == "__main__":
    main()
