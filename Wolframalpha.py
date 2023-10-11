import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QTextEdit, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon
import requests

class MathSolverApp(QWidget):
    def __init__(self):
        super().__init__()

        self.API_URL = "http://api.wolframalpha.com/v2/query"

        # Initialize API key
        self.API_KEY = self.get_api_key()
        if self.API_KEY is None:
            self.prompt_for_api_key()

        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('AI Math Solver Microbot')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('wolf.png'))  # Set the application icon

        # Widgets
        label = QLabel('Enter your question:')
        self.entry = QLineEdit()

        solve_button = QPushButton('🔍 Solve')
        solve_button.clicked.connect(self.solve)

        quit_button = QPushButton('❌ Quit')
        quit_button.clicked.connect(self.quit_and_open_t)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.entry)
        layout.addWidget(solve_button)
        layout.addWidget(quit_button)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def solve(self):
        query = self.entry.text()
        response = self.get_wolfram_alpha_response(query)
        self.output.setPlainText(response)

    def quit_and_open_t(self):
        # Add your logic for quitting and opening another file
        self.close()

    def get_wolfram_alpha_response(self, query):
        if self.API_KEY is None:
            return "Wolfram Alpha API key not found. Please provide a valid API key."

        params = {
            "input": query,
            "format": "plaintext",
            "output": "JSON",
            "appid": self.API_KEY,
            "podstate": "Step-by-step solution"
        }

        try:
            response = requests.get(self.API_URL, params=params)
            data = response.json()
            result = data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
            return result
        except (KeyError, IndexError):
            return "Sorry, I couldn't find an answer."
        except requests.RequestException:
            return "Oops! Something went wrong while querying Wolfram Alpha."

    def get_api_key(self):
        try:
            with open("WolframAlphaapi.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

    def save_api_key(self, api_key):
        with open("WolframAlphaapi.txt", "w") as file:
            file.write(api_key)

    def prompt_for_api_key(self):
        api_key, ok = QInputDialog.getText(self, 'Input', 'Please enter your Wolfram Alpha API key:')
        if ok and api_key:
            self.API_KEY = api_key
            self.save_api_key(api_key)
        else:
            QMessageBox.warning(self, 'Warning', 'API key not provided. The application may not function correctly.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MathSolverApp()
    window.show()
    sys.exit(app.exec_())
