# from https://www.geeksforgeeks.org/find-number-of-solutions-of-a-linear-equation-of-n-variables/
import sys
from typing import List, Dict, NewType, Iterable

Solution = NewType('Solution', List[int])


def solutions(coefficients: List, rhs: int) -> Iterable[Solution]:
    """find number of non-negative solutions for a given linear equation
    O(n * rhs)
    rhs and coefficients coeff[0...n-1]
    :param coefficients:
    :param rhs: right hand side of equation
    :return: count of solutions for given
    """
    n = len(coefficients)
    # 0 = 0 * coeff
    cache: Dict[rhs, List[Solution]] = {0: [(0,) * n]}

    # Fill table in bottom up manner
    for i, coefficient in enumerate(coefficients):
        for j in range(coefficient, rhs + 1):
            solutions = cache.get(j - coefficient)
            if not solutions:
                continue
            for index, sol in enumerate(solutions):
                solutions[index] = (*sol[:i], sol[i] + 1, *sol[i:])
            print(f'\rcoeff: {i}/{len(coefficients)}, tried solution: [{j}/{rhs}], cache memory used: '
                  f'{(sys.getsizeof(cache)) / 1024 / 1024} Gb', end='')

            cache.setdefault(j, []).extend(solutions)
    print(f'cache size: {len(cache)}, solutions: {len(cache[rhs])}')
    return cache[rhs]


if __name__ == '__main__':
    coeff = [2, 2, 5]
    rhs = 100
    from pprint import pprint

    pprint(solutions(coeff, rhs))
