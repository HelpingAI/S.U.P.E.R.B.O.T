import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextBrowser, QVBoxLayout, QHBoxLayout, QSizePolicy, QProgressBar, QTextEdit
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import requests

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

class WikipediaMicrobotGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.search_history = []

    def init_ui(self):
        self.setWindowTitle("Wikipedia Microbot")
        self.setGeometry(100, 100, 800, 600)

        # Load logo
        logo_pixmap = QPixmap("C:\\Users\\hp\\Desktop\\DEVELOPER\\S.U.P.E.R.B.O.T\\wiki.png")
        icon = QIcon(logo_pixmap)
        self.setWindowIcon(icon)

        # Create widgets
        self.query_label = QLabel("Enter Query:")
        self.query_entry = QLineEdit(self)
        self.search_button = QPushButton("Search", self)
        self.show_history_button = QPushButton("Show History", self)
        self.clear_output_button = QPushButton("Clear Output", self)
        self.quit_button = QPushButton("Quit", self)
        self.output_area = QTextBrowser(self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)

        # Set up font
        font = QFont()
        font.setPointSize(12)
        self.query_entry.setFont(font)
        self.search_button.setFont(font)
        self.show_history_button.setFont(font)
        self.clear_output_button.setFont(font)
        self.quit_button.setFont(font)
        self.output_area.setFont(font)

        # Set up size policies
        self.query_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.search_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.show_history_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.clear_output_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.quit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.output_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Connect signals to slots
        self.search_button.clicked.connect(self.search)
        self.show_history_button.clicked.connect(self.show_search_history)
        self.clear_output_button.clicked.connect(self.clear_output)
        self.quit_button.clicked.connect(self.quit_microbot)

        # Layout
        vbox = QVBoxLayout()
        hbox_query = QHBoxLayout()
        hbox_buttons = QHBoxLayout()

        hbox_query.addWidget(self.query_label)
        hbox_query.addWidget(self.query_entry)
        hbox_query.addWidget(self.search_button)

        hbox_buttons.addWidget(self.show_history_button)
        hbox_buttons.addWidget(self.clear_output_button)
        hbox_buttons.addWidget(self.quit_button)

        hbox_buttons.addWidget(self.progress_bar)

        vbox.addLayout(hbox_query)
        vbox.addWidget(self.output_area)
        vbox.addLayout(hbox_buttons)

        self.setLayout(vbox)

        # Create a worker thread
        self.worker = WikipediaWorker()

    def search(self):
        query = self.query_entry.text()
        if query:
            self.output_area.clear()
            self.progress_bar.setVisible(True)

            # Connect the worker's signals to the corresponding slots
            self.worker.result_received.connect(self.display_result)
            self.worker.error_received.connect(self.display_error)

            # Set the query for the worker
            self.worker.set_query(query)

            # Start the worker thread
            self.worker.start()

            # Add the query to the search history
            self.search_history.append(query)

    def display_result(self, result):
        self.worker.result_received.disconnect(self.display_result)
        self.progress_bar.setVisible(False)
        self.output_area.setHtml(result)

    def display_error(self, error_message):
        self.worker.error_received.disconnect(self.display_error)
        self.progress_bar.setVisible(False)
        self.output_area.append(f"Error: {error_message}")

    def show_search_history(self):
        history_text = "\n".join(self.search_history)
        if history_text:
            self.output_area.append(f"Search History:\n{history_text}")
        else:
            self.output_area.append("Search history is empty.")

    def clear_output(self):
        self.output_area.clear()

    def quit_microbot(self):
        self.close()

class WikipediaWorker(QThread):
    result_received = pyqtSignal(str)
    error_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.query = ""

    def set_query(self, query):
        self.query = query

    def run(self):
        try:
            result = self.get_wiki_result(self.query)
            self.result_received.emit(result)
        except Exception as e:
            self.error_received.emit(str(e))

    def get_wiki_result(self, query):
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|images|info",
            "exintro": True,
            "explaintext": True,
            "exsectionformat": "plain",
            "titles": query,
            "utf8": 1,
            "formatversion": 2
        }

        response = requests.get(WIKIPEDIA_API_URL, params=params)
        data = response.json()

        if "error" in data:
            raise Exception(data["error"]["info"])

        page = data["query"]["pages"][0]

        summary = page.get("extract", "")
        html_content = self.create_html_content(page)

        return f"<h1>{page['title']}</h1>{html_content}"

    def create_html_content(self, page):
        html_content = page.get("extract", "")

        # Add clickable image URLs
        for image in page.get("images", []):
            image_url = self.get_image_url(image)
            if image_url:
                html_content += f"<p><a href='{image_url}'>{image['title']}</a></p>"

        return html_content

    def get_image_url(self, image):
        filename = image.get("title", "")
        if filename:
            filename = filename.replace("File:", "")
            return f"https://en.wikipedia.org/wiki/File:{filename}"
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WikipediaMicrobotGUI()
    gui.show()
    sys.exit(app.exec_())
