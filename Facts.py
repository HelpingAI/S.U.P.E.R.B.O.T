import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtGui import QIcon
import requests
from PyQt5.QtCore import Qt

API_URL = "https://useless-facts.sameerkumar.website/api"

class RandomFactsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Random Facts App')
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon('facts.png'))  # Replace with the actual file path

        # Stacked widget for multiple screens
        self.stacked_widget = QStackedWidget(self)

        # Screen 1: Welcome
        welcome_screen = QWidget()
        welcome_layout = QVBoxLayout(welcome_screen)
        welcome_label = QLabel('Welcome to the Random Facts App!')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_label)

        # Screen 2: Facts
        facts_screen = QWidget()
        facts_layout = QVBoxLayout(facts_screen)
        self.facts_label = QLabel()
        facts_layout.addWidget(self.facts_label)

        # Add screens to stacked widget
        self.stacked_widget.addWidget(welcome_screen)
        self.stacked_widget.addWidget(facts_screen)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)

        # Buttons
        fetch_button = QPushButton('Fetch Random Facts', self)
        fetch_button.clicked.connect(self.fetch_facts)
        main_layout.addWidget(fetch_button)

        quit_button = QPushButton('Quit', self)
        quit_button.clicked.connect(self.close)
        main_layout.addWidget(quit_button)

    def fetch_facts(self):
        num_facts = 5  # Adjust the number of facts as needed
        random_facts = self.get_random_facts(num_facts)

        facts_text = ""
        for i, fact in enumerate(random_facts, start=1):
            facts_text += f"{i}. {fact}\n"

        percentage_known = self.calculate_percentage(num_facts)
        facts_text += f"\nYou now know {percentage_known:.2f}% of the world's random facts!"

        self.facts_label.setText(facts_text)

        # Switch to the facts screen
        self.stacked_widget.setCurrentIndex(1)

    def get_random_facts(self, num_facts):
        facts = []

        for _ in range(num_facts):
            response = requests.get(API_URL)

            if response.status_code == 200:
                data = response.json()
                facts.append(data["data"])

        return facts

    def calculate_percentage(self, num_facts, total_population=7_900_000_000):
        return (num_facts / total_population) * 100

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the application icon
    app_icon = QIcon('facts.png')  # Replace with the actual file path
    app.setWindowIcon(app_icon)

    main_window = RandomFactsApp()
    main_window.show()

    sys.exit(app.exec_())
