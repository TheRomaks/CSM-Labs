import json
from pulp import LpProblem, LpMaximize, LpVariable, value
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog

def get_max_profit(json_input):
    if isinstance(json_input, str):
        data = json.loads(json_input)
    else:
        data = json_input

    profit = data['profit']
    material_matrix = data['material_matrix']
    material_limits = data['material_limits']
    products=data['products']

    model = LpProblem("Maximize_profit", LpMaximize)
    variables = [LpVariable(f"x{i + 1}", lowBound=0, cat='Integer') for i in range(len(profit))]
    model += sum(profit[i] * variables[i] for i in range(len(profit)))

    for i in range(len(material_matrix)):
        model += sum(material_matrix[i][j] * variables[j] for j in range(len(variables))) <= material_limits[i]

    model.solve()
    results = {products[i]: value(variables[i]) for i in range(len(variables))}
    return json.dumps({"status": model.status, "results": results}, ensure_ascii=False, indent=4)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optimization Problem Solver")

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        button_load = QPushButton("Load JSON File")
        button_load.clicked.connect(self.load_json_file)
        layout.addWidget(button_load)

        button_calculate = QPushButton("Calculate")
        button_calculate.clicked.connect(self.calculate)
        layout.addWidget(button_calculate)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.json_data = None

    def load_json_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Открыть JSON файл", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'r') as file:
                self.json_data = file.read()
            self.text_edit.setText(self.json_data)

    def calculate(self):
        if self.json_data:
            result = get_max_profit(self.json_data)
            self.text_edit.setText(result)
        else:
            self.text_edit.setText("No JSON file loaded.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
