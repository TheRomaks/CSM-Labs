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
        return self.x/self.m

    def generate(self, n):
        return [self.next() for i in range(n)]

def generate_binomial(n, p, size):
    return np.random.binomial(n, p, size)