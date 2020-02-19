from logic_formula_generator.generators import IntegerRange


class TestIntegerRange:
    def test_absolute_range(self):
        r = IntegerRange(min=10, max=100)
        assert r.min == 10
        assert r.max == 100
        assert r.average == 55.0

    def test_relative_range(self):
        r = IntegerRange.from_relative(number=100, threshold=0.05)
        assert r.min == 95
        assert r.max == 105
        assert r.average == 100.0

    def test_delta_range(self):
        r = IntegerRange.from_relative(number=100, min_delta=20)
        assert r.min == 80
        assert r.max == 120
        assert r.average == 100.0

    def test_delta_and_relative_range(self):
        r = IntegerRange.from_relative(number=100, threshold=0.05, min_delta=20)
        assert r.min == 80
        assert r.max == 120
        assert r.average == 100.0
