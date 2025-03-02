import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel


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


class RandomGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Генератор случайных чисел")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.result_label = QLabel("Результаты генерации:")
        layout.addWidget(self.result_label)

        self.text_output = QTextEdit()
        layout.addWidget(self.text_output)

        self.generate_button = QPushButton("Сгенерировать числа")
        self.generate_button.clicked.connect(self.generate_numbers)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate_numbers(self):
        a, b, c, m, x0 = 6, 7, 3, 4096, 1
        generator = QuadraticCongruentialGenerator(a, b, c, m, x0)

        sample_sizes = [20, 150, 1000]
        generate_analysis = analyze_distribution(generator, sample_sizes, "равномерного распределения")
        binomial_analysis = analyze_distribution(generator, sample_sizes, "биномиального распределения",
                                                 is_binomial=True)

        output_text = "Конгруэнтный метод:\n"
        output_text += "Статистика выборок:\n"
        for size, (mean, var, std_dev, lb, ub, exp_perc, act_perc) in generate_analysis.items():
            output_text += f"n={size}:\n Мат ожидание={mean:.4f},\n Дисперсия={var:.4f},\n Среднее квадратичное отклонение={std_dev:.4f}\n"
            output_text += f"Частотный тест: Интервал=({lb:.4f}, {ub:.4f}), Ожидаемый %={exp_perc:.1f}, Итоговый %={act_perc:.1f}\n"

        output_text += "\nБиномиальное распределение:\n"
        output_text += "Статистика выборок:\n"
        for size, (mean, var, std_dev, lb, ub, exp_perc, act_perc) in binomial_analysis.items():
            output_text += f"n={size}:\n Мат ожидание={mean:.4f},\n Дисперсия={var:.4f},\n Среднее квадратичное отклонение={std_dev:.4f}\n"
            output_text += f"Частотный тест: Интервал=({lb:.4f}, {ub:.4f}), Ожидаемый %={exp_perc:.1f}, Итоговый %={act_perc:.1f}\n"

        self.text_output.setText(output_text)


if __name__ == "__main__":
    app = QApplication([])
    window = RandomGeneratorApp()
    window.show()
    app.exec()
