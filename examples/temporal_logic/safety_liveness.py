import sys

from src.generators.presets.propositional_temporal_logic.propositional_temporal_logic_generator import \
    PropositionalTemporalLogicGenerator

sys.setrecursionlimit(4000)

if __name__ == '__main__':
    gen = PropositionalTemporalLogicGenerator(variable_names={f'V{i}' for i in range(10)},
                                              number_of_variables_with_always_connectives=5,
                                              number_of_variables_with_eventually_connectives=5,
                                              number_of_variables_with_both_connectives=5,
                                              number_of_variables_without_connective=5)
    formula = gen.generate()
    print(str(formula))