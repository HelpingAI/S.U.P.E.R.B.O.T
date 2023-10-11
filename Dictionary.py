import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
import requests
from bs4 import BeautifulSoup

class WordDefinitionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Word Definition App")
        self.setGeometry(100, 100, 500, 500)

        # Set app icon
        self.setWindowIcon(QIcon('app_icon.png'))  # Replace 'app_icon.png' with your icon file

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.word_label = QLabel("Enter a word:")
        self.word_entry = QLineEdit()
        self.definition_label = QLabel("Definition:")
        self.definition_output = QTextEdit()
        self.definition_output.setReadOnly(True)

        self.get_definition_button = QPushButton("Get Definition")
        self.quit_button = QPushButton("Quit")

        self.get_definition_button.clicked.connect(self.get_definition)
        self.quit_button.clicked.connect(self.quit_and_open_superbot)

        layout.addWidget(self.word_label)
        layout.addWidget(self.word_entry)
        layout.addWidget(self.definition_label)
        layout.addWidget(self.definition_output)
        layout.addWidget(self.get_definition_button)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

    def get_definition(self):
        word = self.word_entry.text().strip()
        if word.lower() == 'quit':
            self.quit_and_open_superbot()
        else:
            definition = self.fetch_definition(word)
            # Display definition in bold using HTML formatting
            self.definition_output.setHtml(f'<b>{definition}</b>')

    def fetch_definition(self, word):
        base_url = f"https://www.merriam-webster.com/dictionary/{word}"

        response = requests.get(base_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            definition_span = soup.find("span", class_="dtText")

            if definition_span:
                full_definition = definition_span.get_text()
                sentences = full_definition.split('. ')
                limited_definition = '. '.join(sentences[:3])
                return limited_definition
            else:
                return "Definition not found."
        else:
            return "Word not found or unable to retrieve data."

    def quit_and_open_superbot(self):
        try:
            # Replace 'SUPERBOT.py' with your script
            QMessageBox.information(self, 'Information', 'Opening SUPERBOT.py...')
            # Uncomment the line below to actually open SUPERBOT.py
            # subprocess.run(["python", "SUPERBOT.py"])
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Error opening SUPERBOT.py: {str(e)}")
        finally:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WordDefinitionApp()
    window.show()
    sys.exit(app.exec_())
