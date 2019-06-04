import random


def random_bool(probability: float = 0.5) -> bool:
    return random.random() < probability
