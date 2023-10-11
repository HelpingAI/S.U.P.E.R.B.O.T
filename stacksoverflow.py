import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextBrowser, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import requests

API_URL = "https://api.stackexchange.com/2.3/search"

class StackOverflowSearchApp(QMainWindow):
    def __init__(self):
        super(StackOverflowSearchApp, self).__init__()

        self.setWindowTitle("Stack Overflow Search Microbot")
        self.setWindowIcon(QIcon('path/to/your/icon.png'))  # Replace 'path/to/your/icon.png' with the actual path to your icon
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label1 = QLabel("Welcome to the Stack Overflow Search Microbot!")
        label2 = QLabel("This microbot can search for solutions on Stack Overflow.")

        self.entry = QLineEdit()

        self.fetch_button = QPushButton("🔍 Fetch Results")
        self.fetch_button.clicked.connect(self.fetch_results)

        self.quit_button = QPushButton("❌ Quit")
        self.quit_button.clicked.connect(self.close)

        self.output_text = QTextBrowser()
        self.output_text.setOpenExternalLinks(True)  # Enable opening links in the default web browser

        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(self.entry)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.quit_button)
        layout.addWidget(self.output_text)

        self.central_widget.setLayout(layout)

    def fetch_results(self):
        query = self.entry.text()
        results = self.search_stack_overflow(query)
        self.output_text.clear()
        self.output_text.setHtml(results)

    def search_stack_overflow(self, query):
        params = {
            "order": "desc",
            "sort": "relevance",
            "intitle": query,
            "site": "stackoverflow"
        }

        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])

            if items:
                results = []
                for item in items:
                    title = item.get("title", "No title")
                    title = self.remove_symbols(title)
                    link = item.get("link", "No link")
                    description = item.get("excerpt", "No description")
                    results.append(f"Title: {title}<br>Description: {description}<br>Link: <a href='{link}'>{link}</a><br>")

                return "".join(results)
            else:
                return "No results found on Stack Overflow."
        else:
            return "Oops! Something went wrong while searching Stack Overflow."

    @staticmethod
    def remove_symbols(text):
        return ''.join(c for c in text if c.isalnum() or c.isspace())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StackOverflowSearchApp()
    window.show()
    sys.exit(app.exec_())
