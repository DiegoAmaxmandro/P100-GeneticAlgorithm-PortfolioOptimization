# Imports
import random
import numpy as np
import pandas as pd
from deap import base, creator, tools
from benchmark_utils import compute_benchmark, load_returns
from evaluation import evaluate_portfolio
import os
import csv

# Parameters
q = 15  
pop_size = 50
ngen = 30
cx_prob = 0.7
mut_prob = 0.2

# Load data
returns = load_returns("returns.csv")
all_stock_simbols = list(returns.columns)

# Creating benchmark
benchmark_returns, _ = compute_benchmark(returns)

# Setting generic algorithm

# Chromosome : list of selected stock simbols
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Randomly creating an individual with q unique stock simbols
toolbox.register("attr_stock", lambda: random.sample(all_stock_simbols, q))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_stock)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Fitness function
def evaluate(individual):
    selected_returns = returns[individual]
    port_returns = selected_returns.mean(axis=1)
    corr = port_returns.corr(benchmark_returns)
    return (corr,) 

toolbox.register("evaluate", evaluate)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)

# Mutation: randomly replace 1 stock
def mutate(individual):
    i = random.randint(0, q - 1)
    available = list(set(all_stock_simbols) - set(individual))
    if available:
        individual[i] = random.choice(available)
    return (individual,)

toolbox.register("mutate", mutate)


# Running the algorithm
def run_ga():
    pop = toolbox.population(n=pop_size)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for gen in range(ngen):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mut_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        # Evaluating invalid fitness
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid)
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring
    
    # Best individual
    best = tools.selBest(pop, 1)[0]
    return best, best.fitness.values[0]

# Running GA
if __name__ == "__main__":
    print("Running GA...")
    best_portfolio, best_score = run_ga()
    print("Best Portfolio:", best_portfolio)
    print("Best Correlation to Benchmark:", best_score)
    
    print("\nEvaluating portfolio...")
    evaluate_portfolio(best_portfolio)
    tracking_error = evaluate_portfolio(best_portfolio)
    
    # Saving the results
    filename = "ga_results.csv"
    header = not os.path.exists(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(["q", "correlation", "tracking_error", "portfolio"])
        writer.writerow([q, best_score, tracking_error, best_portfolio])

    print(f"Results saved to {filename}")
    

