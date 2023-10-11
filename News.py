import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QInputDialog, QLineEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from datetime import datetime, timedelta

class NewsApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api_key = self.get_api_key()
        self.page = 1
        self.page_size = 10

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("News Microbot")

        # Set App Icon
        app_icon = QIcon("news.png")
        self.setWindowIcon(app_icon)

        central_widget = QFrame(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # News Display Area
        self.output_area = QTextEdit(self)
        layout.addWidget(self.output_area)

        # Options Layout (Country, Category, Number of Articles, Number of Pages)
        options_layout = QHBoxLayout()

        self.country_codes = {'India': 'in', 'United States': 'us', 'Australia': 'au', 'United Kingdom': 'gb'}
        self.country_combo = QComboBox(self)
        self.country_combo.addItems(self.country_codes.keys())
        options_layout.addWidget(self.country_combo)

        self.category_combo = QComboBox(self)
        self.category_combo.addItems(['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'])
        options_layout.addWidget(self.category_combo)

        self.articles_label = QLabel("No. of Articles:", self)
        options_layout.addWidget(self.articles_label)
        self.articles_input = QLineEdit(self)
        self.articles_input.setText(str(self.page_size))
        options_layout.addWidget(self.articles_input)

        self.pages_label = QLabel("No. of Pages:", self)
        options_layout.addWidget(self.pages_label)
        self.pages_input = QLineEdit(self)
        self.pages_input.setText(str(self.page))
        options_layout.addWidget(self.pages_input)

        layout.addLayout(options_layout)

        # Button Layout (Fetch, More, Quit, Speak News)
        button_layout = QHBoxLayout()

        self.fetch_button = QPushButton("Fetch News", self)
        self.fetch_button.clicked.connect(self.fetch_news)
        button_layout.addWidget(self.fetch_button)

        self.more_button = QPushButton("More", self)
        self.more_button.clicked.connect(self.fetch_news)
        button_layout.addWidget(self.more_button)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.quit_program)
        button_layout.addWidget(self.quit_button)

        self.speak_button = QPushButton("Speak News", self)
        self.speak_button.clicked.connect(self.speak_news)
        button_layout.addWidget(self.speak_button)

        layout.addLayout(button_layout)

        # Status Labels (Message, Reset Timer)
        status_layout = QHBoxLayout()

        self.message_label = QLabel("", self)
        status_layout.addWidget(self.message_label)

        self.reset_timer_label = QLabel("Reset Time: ", self)
        status_layout.addWidget(self.reset_timer_label)

        layout.addLayout(status_layout)

        self.update_reset_timer()

    def get_api_key(self):
        try:
            with open('newsAPI.txt', 'r') as file:
                api_key = file.read().strip()
        except (FileNotFoundError, IOError):
            api_key, ok = QInputDialog.getText(self, 'Input', 'Enter your NewsAPI key:')
            if ok:
                with open('newsAPI.txt', 'w') as file:
                    file.write(api_key)
            else:
                self.show_message("API key cannot be empty.", "red")
                sys.exit()

        return api_key

    def get_news(self, country='in', category=None, page=1, page_size=10):
        endpoint = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": country,
            "apiKey": self.api_key,
            "page": page,
            "pageSize": page_size
        }
        if category:
            params['category'] = category

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            return articles
        else:
            return None

    def fetch_news(self):
        try:
            self.page_size = int(self.articles_input.text())
            self.page = int(self.pages_input.text())
        except ValueError:
            self.show_message("Please enter valid numbers for Articles and Pages.", "red")
            return

        country = self.country_codes[self.country_combo.currentText()]
        category = self.category_combo.currentText()
        news_articles = self.get_news(country, category, self.page, self.page_size)

        if news_articles:
            self.output_area.clear()
            for i, article in enumerate(news_articles, start=(self.page - 1) * self.page_size + 1):
                bold_title = f"<b>Title:</b> {article.get('title', 'No title')}"
                colored_source = f"<font color='blue'><i>Source:</i> {article.get('source', {}).get('name', 'Unknown source')}</font>"
                description = f"<font color='green'><i>Description:</i> {article.get('description', 'Not available')}</font>"

                self.output_area.insertHtml(f"<font color='purple'><b>Article {i}</b></font><br>{bold_title}<br>{colored_source}<br>{description}<br><font color='orange'>{'=' * 50}</font><br>")
        else:
            self.show_message("Failed to fetch news.", "red")

        self.page += 1

    def speak_news(self):
        self.show_message("This feature has been removed in this version.", "blue")

    def update_reset_timer(self):
        reset_time = datetime.now() + timedelta(days=1)
        self.reset_timer_label.setText(f"<i>Reset Time:</i> {reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
        QTimer.singleShot(1000, self.update_reset_timer)

    def save_query_count_on_exit(self):
        # No query count to save
        pass

    def quit_program(self):
        sys.exit()

    def show_message(self, message, color):
        self.message_label.setText(f"<font color='{color}'>{message}</font>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NewsApp()
    window.show()
    sys.exit(app.exec_())
