import base64
import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QFormLayout, QGraphicsScene, QGraphicsView, QMessageBox,
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from Lab2.physics_task import drop_ball_in_liquid

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Падение шара в жидкости")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        form_layout = QFormLayout()
        self.r_input = QLineEdit("0.17")
        self.g_input = QLineEdit("9.81")
        self.ball_density_input = QLineEdit("7850")
        self.liquid_density_input = QLineEdit("1260")
        self.mu_input = QLineEdit("0.001")
        self.h_input = QLineEdit("2")

        form_layout.addRow("Радиус шара (м):", self.r_input)
        form_layout.addRow("Ускорение свободного падения (м/с²):", self.g_input)
        form_layout.addRow("Плотность шара (кг/м³):", self.ball_density_input)
        form_layout.addRow("Плотность жидкости (кг/м³):", self.liquid_density_input)
        form_layout.addRow("Вязкость жидкости (Па·с):", self.mu_input)
        form_layout.addRow("Начальная высота (м):", self.h_input)

        calculate_button_form = QPushButton("Выполнить расчет")
        calculate_button_form.clicked.connect(self.perform_calculation_from_form)
        form_layout.addRow(calculate_button_form)

        layout.addLayout(form_layout)

        self.graphics_view = QGraphicsView()
        layout.addWidget(self.graphics_view)

    def perform_calculation_from_form(self):
        try:
            r = self.validate_positive_float(self.r_input.text(), "Радиус шара")
            g = self.validate_positive_float(self.g_input.text(), "Ускорение свободного падения")
            ball_density = self.validate_positive_float(self.ball_density_input.text(), "Плотность шара")
            liquid_density = self.validate_positive_float(self.liquid_density_input.text(), "Плотность жидкости")
            mu = self.validate_positive_float(self.mu_input.text(), "Вязкость жидкости")
            h = self.validate_positive_float(self.h_input.text(), "Начальная высота")

            img_b64 = drop_ball_in_liquid(r, g, ball_density, liquid_density, mu, h)

            self.display_image(img_b64)
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def validate_positive_float(self, value, field_name):
        try:
            float_value = float(value)
            if float_value < 0:
                raise ValueError(f"{field_name} не может быть отрицательным.")
            return float_value
        except ValueError:
            raise ValueError(f"Введите корректное положительное числовое значение для поля '{field_name}'.")

    def display_image(self, img_b64):
        img_data = base64.b64decode(img_b64)
        img = QImage.fromData(img_data)
        pixmap = QPixmap.fromImage(img)

        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.graphics_view.setScene(scene)
        self.graphics_view.fitInView(scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
