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
    fig, axes = plt.subplots(1, len(sample_sizes), figsize=(5 * len(sample_sizes), 5))

    if len(sample_sizes) == 1:
        axes = [axes]

    for ax, size in zip(axes, sample_sizes):
        if is_binomial:
            sample = generate_binomial(20, 0.75, size) / 20
        else:
            sample = generator.generate(size)
        mean = np.mean(sample)
        variance = np.var(sample)
        std_dev = np.std(sample)
        lower_bound, upper_bound, expected_percentage, actual_percentage = frequency_test(sample)
        results[size] = (mean, variance, std_dev, lower_bound, upper_bound, expected_percentage, actual_percentage)

        ax.hist(sample, bins=20, alpha=0.7)
        ax.set_title(f"n = {size}")
        ax.set_xlabel("Значение")
        ax.set_ylabel("Частота")

    fig.suptitle(f"Гистограмма {title}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    return results
