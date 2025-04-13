import unittest
from generator import QuadraticCongruentialGenerator, generate_binomial
from analyze import frequency_test

class TestQuadraticCongruentialGenerator(unittest.TestCase):
    def test_next_value_in_range(self):
        gen = QuadraticCongruentialGenerator(a=1, b=1, c=1, m=7, x0=0)
        val = gen.next()
        self.assertGreaterEqual(val, 0.0, "Значение должно быть >= 0")
        self.assertLess(val, 1.0, "Значение должно быть < 1")

    def test_generate_length_and_range(self):
        gen = QuadraticCongruentialGenerator(a=1, b=1, c=1, m=7, x0=0)
        n = 10
        sequence = gen.generate(n)
        self.assertEqual(len(sequence), n, "Длина последовательности должна совпадать с n")
        for val in sequence:
            self.assertGreaterEqual(val, 0.0)
            self.assertLess(val, 1.0)

class TestGenerateBinomial(unittest.TestCase):
    def test_generate_binomial_output(self):
        n, p, size = 10, 0.5, 100
        samples = generate_binomial(n, p, size)
        self.assertEqual(len(samples), size, "Размер выходного массива должен быть равен size")
        self.assertTrue(all(0 <= x <= n for x in samples),
                        "Значения биномиальной выборки должны лежать в диапазоне [0, n]")

class TestAnalyze(unittest.TestCase):
    def test_frequency_test(self):
        sample = [0.2, 0.3, 0.5, 0.75, 0.9]
        lower_bound, upper_bound, expected_percentage, actual_percentage = frequency_test(sample)

        self.assertEqual(lower_bound, 0.2113, msg="Нижняя граница не совпадает с ожидаемой")
        self.assertEqual(upper_bound, 0.7887, msg="Верхняя граница не совпадает с ожидаемой")
        self.assertEqual(expected_percentage, 57.7, msg="Ожидаемый процент не совпадает")
        self.assertEqual(actual_percentage, 60.0,  msg="Фактический процент не совпадает с расчётным")


if __name__ == '__main__':
    unittest.main()
