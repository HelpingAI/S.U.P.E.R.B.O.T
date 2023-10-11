import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton
from PyQt5.QtGui import QIcon
import requests
import random

class MotivationalQuoteApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set the application icon
        self.setWindowIcon(QIcon('mot.png')) 

        self.setWindowTitle('Motivational Quote Microbot')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        self.quote_label = QLabel(self)
        layout.addWidget(self.quote_label)

        get_quote_button = QPushButton('💡 Get Quote', self)
        get_quote_button.clicked.connect(self.display_quote)
        layout.addWidget(get_quote_button)

        quit_button = QPushButton('🚪 Quit', self)
        quit_button.clicked.connect(self.quit_app)
        layout.addWidget(quit_button)

        self.setLayout(layout)

    def get_motivational_quote(self):
        url = "https://type.fit/api/quotes"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            quotes = random.sample(data, 5)
            return [quote["text"] for quote in quotes]
        else:
            return ["Oops! Something went wrong while fetching the quote. :("]

    def format_quote(self, quotes):
        emojis = ["💪", "🌟", "🔥", "💫"]
        formatted_quotes = []
        for quote in quotes:
            formatted_quote = f"---------------\n{random.choice(emojis)} {quote} {random.choice(emojis)}\n---------------"
            formatted_quotes.append(formatted_quote)
        return "\n".join(formatted_quotes)

    def display_quote(self):
        quotes = self.get_motivational_quote()
        formatted_quotes = self.format_quote(quotes)
        self.text_edit.clear()
        self.text_edit.setPlainText(formatted_quotes)

    def quit_app(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the application style (optional)
    app.setStyle('Fusion')

    window = MotivationalQuoteApp()
    window.show()

    sys.exit(app.exec_())
