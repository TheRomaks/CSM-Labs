import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QDoubleSpinBox, QSpinBox, QCheckBox, QPushButton, QTextEdit,
    QMessageBox, QLineEdit
)
from Lab4.analyze import analyze_distribution
from Lab4.generator import QuadraticCongruentialGenerator
from Lab5.diagnostics import run_analytical
from Lab5.diagnostics_simpy import run_simulation
from Lab5.station import AnalyticalModel
from Lab5.station_simpy import SimulationModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Симуляция и аналитический расчёт диагностики")
        self.resize(900, 700)
        self.init_ui()

    def init_ui(self):
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.simulation_tab = QWidget()
        self.tab_widget.addTab(self.simulation_tab, "Диагностика")
        main_layout = QVBoxLayout(self.simulation_tab)

        sim_params_layout = QFormLayout()
        self.lambda_input = QDoubleSpinBox()
        self.lambda_input.setRange(0.01, 100.0)
        self.lambda_input.setValue(0.5)
        self.lambda_input.setSingleStep(0.1)
        sim_params_layout.addRow("λ (интенсивность поступления):", self.lambda_input)

        self.service_time_input = QDoubleSpinBox()
        self.service_time_input.setRange(0.01, 100.0)
        self.service_time_input.setValue(1.2)
        self.service_time_input.setSingleStep(0.1)
        sim_params_layout.addRow("Tобсл (время обслуживания):", self.service_time_input)

        self.sim_time_input = QSpinBox()
        self.sim_time_input.setRange(1, 10000)
        self.sim_time_input.setValue(1000)
        sim_params_layout.addRow("Время симуляции (для SimPy):", self.sim_time_input)

        self.use_simpy_checkbox = QCheckBox("Использовать SimPy")
        self.use_simpy_checkbox.setChecked(True)
        sim_params_layout.addRow(self.use_simpy_checkbox)

        main_layout.addLayout(sim_params_layout)

        gen_params_layout = QFormLayout()
        self.gen_a_input = QSpinBox()
        self.gen_a_input.setRange(0, 10000)
        self.gen_a_input.setValue(6)
        gen_params_layout.addRow("Параметр a:", self.gen_a_input)

        self.gen_b_input = QSpinBox()
        self.gen_b_input.setRange(0, 10000)
        self.gen_b_input.setValue(7)
        gen_params_layout.addRow("Параметр b:", self.gen_b_input)

        self.gen_c_input = QSpinBox()
        self.gen_c_input.setRange(0, 10000)
        self.gen_c_input.setValue(3)
        gen_params_layout.addRow("Параметр c:", self.gen_c_input)

        self.gen_m_input = QSpinBox()
        self.gen_m_input.setRange(1, 1000000)
        self.gen_m_input.setValue(4096)
        gen_params_layout.addRow("Параметр m:", self.gen_m_input)

        self.gen_x0_input = QSpinBox()
        self.gen_x0_input.setRange(0, 1000000)
        self.gen_x0_input.setValue(1)
        gen_params_layout.addRow("Начальное значение x0:", self.gen_x0_input)

        main_layout.addLayout(gen_params_layout)

        test_params_layout = QFormLayout()
        self.sample_sizes_input = QLineEdit("10,25,100,500,1000")
        test_params_layout.addRow("Размеры выборок (через запятую):", self.sample_sizes_input)

        main_layout.addLayout(test_params_layout)

        buttons_layout = QHBoxLayout()
        self.run_button = QPushButton("Запустить расчёт")
        self.run_button.clicked.connect(self.run_calculations)
        buttons_layout.addWidget(self.run_button)

        self.test_button = QPushButton("Анализ распределения генератора")
        self.test_button.clicked.connect(self.run_generator_test)
        buttons_layout.addWidget(self.test_button)

        main_layout.addLayout(buttons_layout)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        self.station_tab = QWidget()
        self.tab_widget.addTab(self.station_tab, "Станция")
        station_layout = QVBoxLayout(self.station_tab)

        station_params_layout = QFormLayout()
        self.station_lambda_input = QDoubleSpinBox()
        self.station_lambda_input.setRange(0.01, 100.0)
        self.station_lambda_input.setValue(1.0)
        self.station_lambda_input.setSingleStep(0.1)
        station_params_layout.addRow("λ (интенсивность поступления):", self.station_lambda_input)

        self.station_service_time_input = QDoubleSpinBox()
        self.station_service_time_input.setRange(0.01, 100.0)
        self.station_service_time_input.setValue(3.0)
        self.station_service_time_input.setSingleStep(0.1)
        station_params_layout.addRow("Tобсл (время обслуживания):", self.station_service_time_input)

        self.station_num_pumps_input = QSpinBox()
        self.station_num_pumps_input.setRange(1, 100)
        self.station_num_pumps_input.setValue(4)
        station_params_layout.addRow("Число колонок:", self.station_num_pumps_input)

        self.station_max_queue_input = QSpinBox()
        self.station_max_queue_input.setRange(0, 100)
        self.station_max_queue_input.setValue(4)
        station_params_layout.addRow("Макс. длина очереди:", self.station_max_queue_input)

        self.station_sim_time_input = QSpinBox()
        self.station_sim_time_input.setRange(1, 10000)
        self.station_sim_time_input.setValue(1000)
        station_params_layout.addRow("Время симуляции (для SimPy):", self.station_sim_time_input)

        station_layout.addLayout(station_params_layout)

        station_buttons_layout = QHBoxLayout()
        self.run_station_analytical_button = QPushButton("Выполнить аналитический расчёт")
        self.run_station_analytical_button.clicked.connect(self.run_station_analytical)
        station_buttons_layout.addWidget(self.run_station_analytical_button)

        self.run_station_simulation_button = QPushButton("Запустить симуляцию (SimPy)")
        self.run_station_simulation_button.clicked.connect(self.run_station_simulation)
        station_buttons_layout.addWidget(self.run_station_simulation_button)

        station_layout.addLayout(station_buttons_layout)

        self.station_output_text = QTextEdit()
        self.station_output_text.setReadOnly(True)
        station_layout.addWidget(self.station_output_text)

    def run_calculations(self):
        try:
            lambda_rate = self.lambda_input.value()
            service_time = self.service_time_input.value()
            sim_time = self.sim_time_input.value()
            use_simpy = self.use_simpy_checkbox.isChecked()

            a = self.gen_a_input.value()
            b = self.gen_b_input.value()
            c = self.gen_c_input.value()
            m = self.gen_m_input.value()
            x0 = self.gen_x0_input.value()

            gen = QuadraticCongruentialGenerator(a=a, b=b, c=c, m=m, x0=x0)

            self.output_text.clear()
            self.output_text.append("Сгенерированные значения (через генератор):")
            lambda_gen = gen.next() * 0.5 + 0.25
            t_obsl_gen = gen.next() * 1 + 0.7
            self.output_text.append(f"λ = {lambda_gen:.2f}, Tобсл = {t_obsl_gen:.2f}\n")

            if use_simpy:
                self.output_text.append("Запуск симуляции с использованием SimPy:")
                sim_results = run_simulation(lambda_rate, service_time, sim_time)
                self.output_text.append("Результаты симуляции (SimPy):")
                self.output_text.append(f"P0 (вероятность простоя) = {sim_results['p0']:.4f}")
                if sim_results['p_otkaza'] is not None:
                    self.output_text.append(f"Pотк (вероятность отказа) = {sim_results['p_otkaza']:.4f}")
                    self.output_text.append(f"q (относительная пропускная способность) = {sim_results['q']:.4f}")
                    self.output_text.append(f"A (абсолютная пропускная способность) = {sim_results['A']:.4f}")
                    self.output_text.append(f"Всего автомобилей: {sim_results['total_cars']}")
                    self.output_text.append(f"Обслужено автомобилей: {sim_results['served_cars']}")
                else:
                    self.output_text.append("Нет поступивших автомобилей для расчёта Pотк.")
            else:
                self.output_text.append("Выполнение аналитического расчёта (без SimPy):")
                analytical_results = run_analytical(lambda_rate, service_time)
                self.output_text.append("Результаты аналитического расчёта:")
                self.output_text.append(f"ro = {analytical_results['ro']:.4f}")
                self.output_text.append(f"P0 (вероятность простоя) = {analytical_results['p0']:.4f}")
                self.output_text.append(f"Pотк (вероятность отказа) = {analytical_results['p_otkaza']:.4f}")
                self.output_text.append(f"q (относительная пропускная способность) = {analytical_results['q']:.4f}")
                self.output_text.append(f"A (абсолютная пропускная способность) = {analytical_results['A']:.4f}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def run_generator_test(self):
        try:
            a = self.gen_a_input.value()
            b = self.gen_b_input.value()
            c = self.gen_c_input.value()
            m = self.gen_m_input.value()
            x0 = self.gen_x0_input.value()

            gen = QuadraticCongruentialGenerator(a=a, b=b, c=c, m=m, x0=x0)

            sample_sizes_str = self.sample_sizes_input.text()
            sample_sizes = [int(x.strip()) for x in sample_sizes_str.split(",") if x.strip().isdigit()]

            self.output_text.append("\nЗапуск анализа распределения генератора:")
            results = analyze_distribution(gen, sample_sizes, title="квадратичный конгруэнтный генератор")

            self.output_text.append("Результаты анализа распределения:")
            for size, res in results.items():
                mean, variance, std_dev, lower_bound, upper_bound, expected_percentage, actual_percentage = res
                self.output_text.append(f"Размер выборки: {size}")
                self.output_text.append(f"  Среднее: {mean:.4f}, Дисперсия: {variance:.4f}, Стандартное отклонение: {std_dev:.4f}")
                self.output_text.append(f"  Интервал: [{lower_bound:.4f}, {upper_bound:.4f}]")
                self.output_text.append(f"  Ожидаемый %: {expected_percentage:.2f}, Фактический %: {actual_percentage:.2f}\n")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def run_station_analytical(self):
        try:
            lambda_val = self.station_lambda_input.value()
            service_time = self.station_service_time_input.value()
            num_pumps = self.station_num_pumps_input.value()
            max_queue = self.station_max_queue_input.value()

            model = AnalyticalModel(lambda_val, service_time, num_pumps)
            results_no_limit = model.mmn_no_limit_queue()
            results_limited = model.mmn_limited_queue(max_queue)

            self.station_output_text.clear()
            self.station_output_text.append("Аналитическая модель (без ограничения очереди):")
            for key, value in results_no_limit.items():
                self.station_output_text.append(f"{key}: {value:.4f}")
            self.station_output_text.append("\nАналитическая модель (с ограниченной очередью):")
            for key, value in results_limited.items():
                self.station_output_text.append(f"{key}: {value:.4f}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def run_station_simulation(self):
        try:
            lambda_val = self.station_lambda_input.value()
            service_time = self.station_service_time_input.value()
            num_pumps = self.station_num_pumps_input.value()
            max_queue = self.station_max_queue_input.value()
            sim_time = self.station_sim_time_input.value()

            sim_model = SimulationModel(lambda_val, service_time, num_pumps, simulation_time=sim_time)
            results_no_limit = sim_model.run_simulation(queue_limit=None)
            results_limited = sim_model.run_simulation(queue_limit=max_queue)

            self.station_output_text.clear()
            self.station_output_text.append("Симуляция модели (без ограничения очереди):")
            for key, value in results_no_limit.items():
                if isinstance(value, int):
                    self.station_output_text.append(f"{key}: {value}")
                else:
                    self.station_output_text.append(f"{key}: {value:.4f}")

            self.station_output_text.append("\nСимуляция модели (с ограниченной очередью):")
            for key, value in results_limited.items():
                if isinstance(value, int):
                    self.station_output_text.append(f"{key}: {value}")
                else:
                    self.station_output_text.append(f"{key}: {value:.4f}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
