import numpy as np
from matplotlib import pyplot as plt

from Lab4.generator import generate_binomial


def frequency_test(sample):
    lower_bound, upper_bound = 0.2113, 0.7887
    expected_percentage = 57.7
    count_in_interval = sum(lower_bound <= x <= upper_bound for x in sample)
    actual_percentage = (count_in_interval / len(sample)) * 100
    return lower_bound, upper_bound, expected_percentage, actual_percentage


def analyze_distribution(generator, sample_sizes, title, is_binomial=False):
    results = {}
    plt.figure(figsize=(10, 5))
    for size in sample_sizes:
        if is_binomial:
            sample = generate_binomial(20, 0.75, size) / 20
        else:
            sample = generator.generate(size)
        mean = np.mean(sample)
        variance = np.var(sample)
        std_dev = np.std(sample)
        lower_bound, upper_bound, expected_percentage, actual_percentage = frequency_test(sample)
        results[size] = (mean, variance, std_dev, lower_bound, upper_bound, expected_percentage, actual_percentage)
        plt.hist(sample, bins=20, alpha=0.5, label=f"n={size}")

    plt.legend()
    plt.title(f"Гистограмма {title}")
    plt.xlabel("Значение")
    plt.ylabel("Частота")
    plt.show()
    return results