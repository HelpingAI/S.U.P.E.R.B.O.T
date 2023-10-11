from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QToolBar, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Google Maps Clone")
        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setWindowIcon(QIcon("Maps.png"))

        # Create central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(self.central_widget)

        # Create QWebEngineView
        self.web_view = QWebEngineView(self)
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Load Google Maps
        self.web_view.load(QUrl("https://www.google.com/maps"))

        # Add the web view to the layout
        layout.addWidget(self.web_view)

        # Create a toolbar with buttons
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Back button
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.web_view.back)
        toolbar.addWidget(back_button)

        # Forward button
        forward_button = QPushButton("Forward", self)
        forward_button.clicked.connect(self.web_view.forward)
        toolbar.addWidget(forward_button)

        # Reload button
        reload_button = QPushButton("Reload", self)
        reload_button.clicked.connect(self.web_view.reload)
        toolbar.addWidget(reload_button)

        # Home button
        home_button = QPushButton("Home", self)
        home_button.clicked.connect(self.go_to_home)
        toolbar.addWidget(home_button)

        # Search bar
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("Search on Google Maps")
        search_bar.returnPressed.connect(lambda: self.search_on_maps(search_bar.text()))
        toolbar.addWidget(search_bar)

    def search_on_maps(self, query):
        # Function to perform a search on Google Maps
        search_url = f"https://www.google.com/maps/search/{query}"
        self.web_view.load(QUrl(search_url))

    def go_to_home(self):
        # Function to go back to the home page
        self.web_view.load(QUrl("https://www.google.com/maps"))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
