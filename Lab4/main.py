import numpy as np

class QuadraticCongruentialGenerator:
    def __init__(self, a, b, c, m, x0):
        self.a = a
        self.b = b
        self.c = c
        self.m = m
        self.x = x0

    def next(self):
        self.x = (self.a * self.x ** 2 + self.b * self.x + self.c) % self.m
        return self.x

    def generate(self, n):
        return [self.next() for i in range(n)]

    def binomial(self, n, p, size):
        return np.random.binomial(n, p, size)


a = 6
b = 7
c = 3
m = 4096
x0 = 1

qcg = QuadraticCongruentialGenerator(a, b, c, m, x0)

random_numbers = qcg.generate(20)
print("Случайные числа:", random_numbers)

n = 20
p = 0.3
size = 10
binomial_numbers = qcg.binomial(n, p, size)
print("Биномиально распределенные числа:", binomial_numbers)