import sys
import base64
import io
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget,
    QSpinBox, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit

def get_trends(data, poly_degree=2):
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')
    data['x'] = (data['date'] - data['date'].min()).dt.days
    x = data['x'].values
    y = data['value'].values

    def linear(x, a, b): return a * x + b
    def logarithmic(x, a, b): return a * np.log(x + 1) + b
    def exponential(x, a, b): return a * np.exp(b * x)

    def polynomial(x, *params):
        return sum(param * x**i for i, param in enumerate(params))

    lin_params, _ = curve_fit(linear, x, y)
    log_params, _ = curve_fit(logarithmic, x, y)
    exp_params, _ = curve_fit(exponential, x, y)

    initial_guess = [1] * (poly_degree + 1)
    poly_params, _ = curve_fit(polynomial, x, y, p0=initial_guess)

    y_linear = linear(x, *lin_params)
    y_log = logarithmic(x, *log_params)
    y_exp = exponential(x, *exp_params)
    y_poly = polynomial(x, *poly_params)

    r2_lin = r2_score(y, y_linear)
    r2_log = r2_score(y, y_log)
    r2_exp = r2_score(y, y_exp)
    r2_poly = r2_score(y, y_poly)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    models = [
        (y_linear, lin_params, r2_lin, "Линейная"),
        (y_poly, poly_params, r2_poly, f"Полиномиальная (степень {poly_degree})"),
        (y_log, log_params, r2_log, "Логарифмическая"),
        (y_exp, exp_params, r2_exp, "Экспоненциальная"),
    ]

    for ax, (y_pred, params, r2, label) in zip(axes.flat, models):
        ax.scatter(x, y, label="Данные", color="blue")
        ax.plot(x, y_pred, label=f"{label} линия тренда", color="red")
        ax.set_title(f"{label} модель: $R^2={r2:.4f}$")
        ax.legend()

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return {"image_url": f"data:image/png;base64,{img_b64}"}

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графический анализ CSV")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        degree_layout = QHBoxLayout()
        self.poly_degree_label = QLabel("Степень полинома:")
        self.poly_degree_spinbox = QSpinBox()
        self.poly_degree_spinbox.setValue(2)
        self.poly_degree_spinbox.setMinimum(1)
        self.poly_degree_spinbox.setMaximum(10)
        degree_layout.addWidget(self.poly_degree_label)
        degree_layout.addWidget(self.poly_degree_spinbox)
        layout.addLayout(degree_layout)

        self.upload_button = QPushButton("Загрузить CSV файл")
        self.upload_button.clicked.connect(self.load_csv)
        layout.addWidget(self.upload_button)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def load_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Открыть CSV файл", "", "CSV Files (*.csv)")
        if file_path:
            try:
                data = pd.read_csv(file_path)
                poly_degree = self.poly_degree_spinbox.value()
                result = get_trends(data, poly_degree=poly_degree)
                image_data = result["image_url"]
                pixmap = QPixmap()
                pixmap.loadFromData(base64.b64decode(image_data.split(',')[1]))
                self.image_label.setPixmap(pixmap.scaledToWidth(700))
            except Exception as e:
                print(f"Ошибка обработки файла: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())