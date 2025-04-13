import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QWidget, QTabWidget, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox, QHBoxLayout
)
from task1.koshi import solution as koshi_solution
from task2.systemdiff import solution as systemdiff_solution
from task3.doublediff import solution as doublediff_solution
from task4.predator_prey import solution as predator_prey_solution
from task4.competition import solution as competition_solution
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Решение дифференциальных уравнений")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_koshi_tab()
        self.create_systemdiff_tab()
        self.create_doublediff_tab()
        self.create_predator_prey_tab()

    def create_koshi_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Численное решение дифференциальных уравнений из koshi.py")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        t0_label = QLabel("Начальное значение t (t0):")
        layout.addWidget(t0_label)
        self.koshi_t0_input = QDoubleSpinBox()
        self.koshi_t0_input.setRange(-100, 100)
        self.koshi_t0_input.setValue(0)
        layout.addWidget(self.koshi_t0_input)

        t1_label = QLabel("Конечное значение t (t1):")
        layout.addWidget(t1_label)
        self.koshi_t1_input = QDoubleSpinBox()
        self.koshi_t1_input.setRange(-100, 100)
        self.koshi_t1_input.setValue(1)
        layout.addWidget(self.koshi_t1_input)

        points_label = QLabel("Количество точек разбиения:")
        layout.addWidget(points_label)
        self.koshi_points_input = QSpinBox()
        self.koshi_points_input.setRange(10, 10000)
        self.koshi_points_input.setValue(100)
        layout.addWidget(self.koshi_points_input)

        run_button = QPushButton("Выполнить задачу koshi.py")
        run_button.clicked.connect(self.run_koshi_solution)
        layout.addWidget(run_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Koshi")

    def run_koshi_solution(self):
        t0 = self.koshi_t0_input.value()
        t1 = self.koshi_t1_input.value()
        points = self.koshi_points_input.value()
        koshi_solution(t0, t1, points)

    def create_systemdiff_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Решение системы из systemdiff.py")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        a_label = QLabel("Параметр a:")
        layout.addWidget(a_label)
        self.systemdiff_a_input = QDoubleSpinBox()
        self.systemdiff_a_input.setRange(-100, 100)
        self.systemdiff_a_input.setValue(0.2)
        layout.addWidget(self.systemdiff_a_input)

        b_label = QLabel("Параметр b:")
        layout.addWidget(b_label)
        self.systemdiff_b_input = QDoubleSpinBox()
        self.systemdiff_b_input.setRange(-100, 100)
        self.systemdiff_b_input.setValue(0.2)
        layout.addWidget(self.systemdiff_b_input)

        c_label = QLabel("Параметр c:")
        layout.addWidget(c_label)
        self.systemdiff_c_input = QDoubleSpinBox()
        self.systemdiff_c_input.setRange(-100, 100)
        self.systemdiff_c_input.setValue(5)
        layout.addWidget(self.systemdiff_c_input)

        t0_label = QLabel("Начальное значение t (t0):")
        layout.addWidget(t0_label)
        self.systemdiff_t0_input = QDoubleSpinBox()
        self.systemdiff_t0_input.setRange(-100, 100)
        self.systemdiff_t0_input.setValue(0)
        layout.addWidget(self.systemdiff_t0_input)

        t1_label = QLabel("Конечное значение t (t1):")
        layout.addWidget(t1_label)
        self.systemdiff_t1_input = QDoubleSpinBox()
        self.systemdiff_t1_input.setRange(0.1, 1000)
        self.systemdiff_t1_input.setValue(100)
        layout.addWidget(self.systemdiff_t1_input)

        points_label = QLabel("Количество точек разбиения:")
        layout.addWidget(points_label)
        self.systemdiff_points_input = QSpinBox()
        self.systemdiff_points_input.setRange(10, 10000)
        self.systemdiff_points_input.setValue(100)
        layout.addWidget(self.systemdiff_points_input)

        run_button = QPushButton("Выполнить задачу systemdiff.py")
        run_button.clicked.connect(self.run_systemdiff_solution)
        layout.addWidget(run_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "SystemDiff")

    def run_systemdiff_solution(self):
        a = self.systemdiff_a_input.value()
        b = self.systemdiff_b_input.value()
        c = self.systemdiff_c_input.value()
        t0 = self.systemdiff_t0_input.value()
        t1 = self.systemdiff_t1_input.value()
        points = self.systemdiff_points_input.value()
        systemdiff_solution(a, b, c, t0, t1, points)

    def create_doublediff_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Решение системы второго порядка из doublediff.py")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        a_label = QLabel("Параметр a:")
        layout.addWidget(a_label)
        self.doublediff_a_input = QDoubleSpinBox()
        self.doublediff_a_input.setRange(-100, 100)
        self.doublediff_a_input.setValue(1)
        layout.addWidget(self.doublediff_a_input)

        t_y0_label = QLabel("Начальное значение t для y (t_y0):")
        layout.addWidget(t_y0_label)
        self.doublediff_t_y0_input = QDoubleSpinBox()
        self.doublediff_t_y0_input.setRange(-100, 100)
        self.doublediff_t_y0_input.setValue(0)
        layout.addWidget(self.doublediff_t_y0_input)

        t_y1_label = QLabel("Конечное значение t для y (t_y1):")
        layout.addWidget(t_y1_label)
        self.doublediff_t_y1_input = QDoubleSpinBox()
        self.doublediff_t_y1_input.setRange(0.1, 100)
        self.doublediff_t_y1_input.setValue(2 * np.pi)
        layout.addWidget(self.doublediff_t_y1_input)

        t_z0_label = QLabel("Начальное значение t для z (t_z0):")
        layout.addWidget(t_z0_label)
        self.doublediff_t_z0_input = QDoubleSpinBox()
        self.doublediff_t_z0_input.setRange(-100, 100)
        self.doublediff_t_z0_input.setValue(0)
        layout.addWidget(self.doublediff_t_z0_input)

        t_z1_label = QLabel("Конечное значение t для z (t_z1):")
        layout.addWidget(t_z1_label)
        self.doublediff_t_z1_input = QDoubleSpinBox()
        self.doublediff_t_z1_input.setRange(0.1, 1000)
        self.doublediff_t_z1_input.setValue(30)
        layout.addWidget(self.doublediff_t_z1_input)

        points_y_label = QLabel("Количество точек разбиения для y:")
        layout.addWidget(points_y_label)
        self.doublediff_points_y_input = QSpinBox()
        self.doublediff_points_y_input.setRange(10, 10000)
        self.doublediff_points_y_input.setValue(1000)
        layout.addWidget(self.doublediff_points_y_input)

        points_z_label = QLabel("Количество точек разбиения для z:")
        layout.addWidget(points_z_label)
        self.doublediff_points_z_input = QSpinBox()
        self.doublediff_points_z_input.setRange(10, 10000)
        self.doublediff_points_z_input.setValue(1000)
        layout.addWidget(self.doublediff_points_z_input)

        run_button = QPushButton("Выполнить задачу doublediff.py")
        run_button.clicked.connect(self.run_doublediff_solution)
        layout.addWidget(run_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "DoubleDiff")

    def run_doublediff_solution(self):
        t_y0 = self.doublediff_t_y0_input.value()
        t_y1 = self.doublediff_t_y1_input.value()
        t_z0 = self.doublediff_t_z0_input.value()
        t_z1 = self.doublediff_t_z1_input.value()
        points_y = self.doublediff_points_y_input.value()
        points_z = self.doublediff_points_z_input.value()
        a = self.doublediff_a_input.value()
        doublediff_solution(t_y0, t_y1, t_z0, t_z1, points_y, points_z, a)

    def create_predator_prey_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Модель хищник-жертва и конкуренция")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        t0_label = QLabel("Начальное значение t (t0):")
        layout.addWidget(t0_label)
        self.predator_t0_input = QDoubleSpinBox()
        self.predator_t0_input.setRange(-100, 1000)
        self.predator_t0_input.setValue(0)
        layout.addWidget(self.predator_t0_input)

        t1_label = QLabel("Конечное значение t (t1):")
        layout.addWidget(t1_label)
        self.predator_t1_input = QDoubleSpinBox()
        self.predator_t1_input.setRange(0.1, 2000)
        self.predator_t1_input.setValue(1000)
        layout.addWidget(self.predator_t1_input)

        points_label = QLabel("Количество точек разбиения:")
        layout.addWidget(points_label)
        self.predator_points_input = QSpinBox()
        self.predator_points_input.setRange(10, 10000)
        self.predator_points_input.setValue(1000)
        layout.addWidget(self.predator_points_input)

        r1_label = QLabel("Параметр r1:")
        layout.addWidget(r1_label)
        self.predator_r1_input = QDoubleSpinBox()
        self.predator_r1_input.setRange(0, 10)
        self.predator_r1_input.setValue(0.5)
        layout.addWidget(self.predator_r1_input)

        l1_label = QLabel("Параметр l1:")
        layout.addWidget(l1_label)
        self.predator_l1_input = QDoubleSpinBox()
        self.predator_l1_input.setRange(0, 10)
        self.predator_l1_input.setValue(0.01)
        layout.addWidget(self.predator_l1_input)

        l2_label = QLabel("Параметр l2:")
        layout.addWidget(l2_label)
        self.predator_l2_input = QDoubleSpinBox()
        self.predator_l2_input.setRange(0, 10)
        self.predator_l2_input.setValue(0.01)
        layout.addWidget(self.predator_l2_input)

        beta_label = QLabel("Параметр beta:")
        layout.addWidget(beta_label)
        self.predator_beta_input = QDoubleSpinBox()
        self.predator_beta_input.setRange(0, 10)
        self.predator_beta_input.setValue(0.2)
        layout.addWidget(self.predator_beta_input)

        x0_label = QLabel("Начальное значение x (x0):")
        layout.addWidget(x0_label)
        self.predator_x0_input = QDoubleSpinBox()
        self.predator_x0_input.setRange(0, 100)
        self.predator_x0_input.setValue(25)
        layout.addWidget(self.predator_x0_input)

        y0_label = QLabel("Начальное значение y (y0):")
        layout.addWidget(y0_label)
        self.predator_y0_input = QDoubleSpinBox()
        self.predator_y0_input.setRange(0, 100)
        self.predator_y0_input.setValue(5)
        layout.addWidget(self.predator_y0_input)

        self.competition_checkbox = QCheckBox("Использовать модель конкуренции (competition.py)")
        self.competition_checkbox.stateChanged.connect(self.toggle_competition)
        layout.addWidget(self.competition_checkbox)

        g1_layout = QHBoxLayout()
        self.g1_label = QLabel("Параметр g1:")
        self.g1_label.setEnabled(False)
        g1_layout.addWidget(self.g1_label)
        self.g1_input = QDoubleSpinBox()
        self.g1_input.setRange(0, 1)
        self.g1_input.setValue(0.0005)
        self.g1_input.setDecimals(5)
        self.g1_input.setEnabled(False)
        g1_layout.addWidget(self.g1_input)
        layout.addLayout(g1_layout)

        run_button = QPushButton("Выполнить задачу модели")
        run_button.clicked.connect(self.run_predator_prey_solution)
        layout.addWidget(run_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Predator-Prey")

    def toggle_competition(self):
        if Qt.Checked:
            self.g1_label.setEnabled(True)
            self.g1_input.setEnabled(True)
        else:
            self.g1_label.setEnabled(False)
            self.g1_input.setEnabled(False)

    def run_predator_prey_solution(self):
        t0 = self.predator_t0_input.value()
        t1 = self.predator_t1_input.value()
        points = self.predator_points_input.value()
        r1 = self.predator_r1_input.value()
        l1 = self.predator_l1_input.value()
        l2 = self.predator_l2_input.value()
        beta = self.predator_beta_input.value()
        x0 = self.predator_x0_input.value()
        y0 = self.predator_y0_input.value()

        if self.competition_checkbox.isChecked():
            g1 = self.g1_input.value()
            competition_solution(t0, t1, points, r1, l1, l2, beta, g1, x0, y0)
        else:
            predator_prey_solution(t0, t1, points, r1, l1, l2, beta, x0, y0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
