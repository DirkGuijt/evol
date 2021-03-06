"""
This example demonstrates how logging works in evolutions.
"""

import random
from evol import Population, Evolution


def random_start():
    """
    This function generates a random (x,y) coordinate in the searchspace
    """
    return (random.random() - 0.5) * 20, (random.random() - 0.5) * 20


def func_to_optimise(xy):
    """
    This is the function we want to optimise (maximize)
    """
    x, y = xy
    return -(1-x)**2 - 2*(2-x**2)**2


def pick_random_parents(pop):
    """
    This is how we are going to select parents from the population
    """
    mom = random.choice(pop)
    dad = random.choice(pop)
    return mom, dad


def make_child(mom, dad):
    """
    This is how two parents are going to make a child.
    Note that the output of a tuple, just like the output of `random_start`
    """
    child_x = (mom[0] + dad[0])/2
    child_y = (mom[1] + dad[1])/2
    return child_x, child_y


def add_noise(chromosome, sigma):
    """
    This is a function that will add some noise to the chromosome.
    """
    new_x = chromosome[0] + (random.random()-0.5) * sigma
    new_y = chromosome[1] + (random.random()-0.5) * sigma
    return new_x, new_y


class MyLogger():
    def __init__(self):
        self.i = 0

    def log(self, pop):
        self.i += 1
        best = max([i.fitness for i in pop.evaluate()])
        print(f"the best score i={self.i} => {best}")


if __name__ == "__main__":
    logger = MyLogger()
    random.seed(42)

    pop = Population(chromosomes=[random_start() for _ in range(200)],
                     eval_function=func_to_optimise,
                     maximize=True, concurrent_workers=2)

    evo1 = (Evolution()
            .survive(fraction=0.1)
            .breed(parent_picker=pick_random_parents, combiner=make_child)
            .mutate(mutate_function=add_noise, sigma=0.2)
            .evaluate()
            .callback(logger.log))

    evo2 = (Evolution()
            .survive(n=10)
            .breed(parent_picker=pick_random_parents, combiner=make_child)
            .mutate(mutate_function=add_noise, sigma=0.1)
            .evaluate()
            .callback(logger.log))

    evo3 = (Evolution()
            .repeat(evo1, n=20)
            .repeat(evo2, n=20))

    pop = pop.evolve(evo3, n=3)
