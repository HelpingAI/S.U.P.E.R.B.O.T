import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QIcon

API_URL = "http://openlibrary.org/search.json"

class BookSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Book Search Microbot')
        self.setWindowIcon(QIcon('app_icon.png'))

        layout = QVBoxLayout()

        label1 = QLabel('Welcome to the Book Search Microbot!')
        label2 = QLabel('This microbot can search for books.')

        self.entry = QLineEdit()
        self.fetch_button = QPushButton('🔍 Fetch Books')
        self.fetch_button.clicked.connect(self.fetch_books)

        self.quit_button = QPushButton('❌ Quit')
        self.quit_button.clicked.connect(self.close_app)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(self.entry)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.quit_button)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def search_books(self, query):
        params = {"q": query}
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            if "docs" in data:
                return data["docs"]
        return None

    def fetch_books(self):
        query = self.entry.text()
        books = self.search_books(query)

        self.output_text.clear()

        if books:
            for book in books:
                title = book.get("title", "Unknown Title")
                author = book.get("author_name", ["Unknown Author"])
                publish_year = book.get("first_publish_year", "Unknown Year")

                self.output_text.insertPlainText(f"Title: {title}\nAuthor: {', '.join(author)}\nPublish Year: {publish_year}\n----------------\n")
        else:
            self.output_text.insertPlainText("No books found for the given query.\n")

    def close_app(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Note: You need to replace 'app_icon.png' with the path to your own app icon.
    app_icon = QIcon('app_icon.png')
    app.setWindowIcon(app_icon)

    window = BookSearchApp()
    window.show()

    sys.exit(app.exec_())
