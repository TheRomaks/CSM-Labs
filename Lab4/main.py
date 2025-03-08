from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel

from Lab4.analyze import analyze_distribution
from Lab4.generator import QuadraticCongruentialGenerator

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
        generate_analysis = analyze_distribution(generator, sample_sizes, "конгруэнтного метода")
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
