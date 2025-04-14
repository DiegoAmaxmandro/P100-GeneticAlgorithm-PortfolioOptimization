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
pop_size = 100 # This represents the population size
ngen = 30 #This would be the number of generations
cx_prob = 0.7 # This is the Crossover
mut_prob = 0.2 # This is the multations probabilities

# Loading data
returns = load_returns("returns.csv")
all_stock_simbols = list(returns.columns)

# Creating benchmark
benchmark_returns, _ = compute_benchmark(returns)

# Running the genetic algorithm
def run_ga(q):
    # Setting up DEAP toolbox for this q
    if "FitnessMax" not in creator.__dict__:
        creator.create("FitnessMax", base.Fitness, weights = (1.0,))
    if "Individual" not in creator.__dict__:
        creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()

    toolbox.register("attr_stock", lambda: random.sample(all_stock_simbols, q))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_stock)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        selected_returns = returns[individual]
        port_returns = selected_returns.mean(axis = 1)
        corr = port_returns.corr(benchmark_returns)
        return (corr,)

    toolbox.register("evaluate", evaluate)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxTwoPoint)

    def mutate(individual):
        i = random.randint(0, q - 1)
        available = list(set(all_stock_simbols) - set(individual))
        if available:
            individual[i] = random.choice(available)
        return (individual,)

    toolbox.register("mutate", mutate)

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
    correlation = best.fitness.values[0]
    tracking_error = evaluate_portfolio(best)
    return q, correlation, tracking_error, best 

# Running GA
if __name__ == "__main__":
    results = []
    print("Running Genetic Algorithm across different q values...\n")
    for q in [10, 11, 12, 13, 14, 15, 20, 25, 30, 40, 50]:
        if q > len(all_stock_simbols):
            print(f"Skipping q = {q} — not enough valid stocks ({len(all_stock_simbols)} available)")
            continue

        print(f"\nRunning GA for q = {q}")
        q_val, correlation, tracking_error, best_portfolio = run_ga(q)
        results.append([q_val, correlation, tracking_error, best_portfolio])

        print(f"Best Portfolio for q = {q}:")
        print(f"Correlation to Benchmark: {correlation:.4f}")
        print(f"Tracking Error: {tracking_error:.4f}")
        print(f"Selected Portfolio: {best_portfolio}")
        print(f"Total stocks available: {len(all_stock_simbols)}")
        print(f"Data length (days): {returns.shape[0]}")

        print("\n Evaluating per-quarter performance breakdown...")
        evaluate_portfolio(best_portfolio)

    # Saving all results
    with open("ga_q_experiments.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["q", "correlation", "tracking_error", "portfolio"])
        writer.writerows(results)

    print("\n Results saved to ga_q_experiments.csv")
    

