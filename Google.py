from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QPushButton, QVBoxLayout, QWidget, QProgressBar, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Google Clone")
        self.setWindowIcon(QIcon("Google.jpeg"))

        # Create central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(self.central_widget)

        # Create QWebEngineView
        self.web_view = QWebEngineView(self)
        self.web_view.setUrl(QUrl("https://www.google.com/"))

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
        search_bar.setPlaceholderText("Search Google")
        search_bar.returnPressed.connect(lambda: self.search_on_google(search_bar.text()))
        toolbar.addWidget(search_bar)

        # History button
        history_button = QPushButton("History", self)
        history_button.clicked.connect(self.show_history)
        toolbar.addWidget(history_button)

        # Bookmarks button
        bookmarks_button = QPushButton("Bookmarks", self)
        bookmarks_button.clicked.connect(self.show_bookmarks)
        toolbar.addWidget(bookmarks_button)

        # Zoom In button
        zoom_in_button = QPushButton("Zoom In", self)
        zoom_in_button.clicked.connect(self.zoom_in)
        toolbar.addWidget(zoom_in_button)

        # Zoom Out button
        zoom_out_button = QPushButton("Zoom Out", self)
        zoom_out_button.clicked.connect(self.zoom_out)
        toolbar.addWidget(zoom_out_button)

        # Download button
        download_button = QPushButton("Download", self)
        download_button.clicked.connect(self.download_file)
        toolbar.addWidget(download_button)

        # Progress Bar
        progress_bar = QProgressBar(self)
        progress_bar.setMaximum(100)
        progress_bar.setValue(0)
        toolbar.addWidget(progress_bar)

        # Connect progress events to update the progress bar
        self.web_view.loadProgress.connect(progress_bar.setValue)
        self.web_view.loadFinished.connect(lambda: progress_bar.setValue(100))

        # Browsing history table
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Title", "URL"])

        # Bookmarks table
        self.bookmarks_table = QTableWidget(self)
        self.bookmarks_table.setColumnCount(2)
        self.bookmarks_table.setHorizontalHeaderLabels(["Title", "URL"])

    def go_to_home(self):
        self.web_view.setUrl(QUrl("https://www.google.com/"))

    def search_on_google(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        self.web_view.setUrl(QUrl(search_url))

    def show_history(self):
        # Retrieve and display browsing history
        history = self.web_view.history()
        self.show_table_dialog("Browsing History", self.history_table, history)

    def show_bookmarks(self):
        # Retrieve and display bookmarks
        bookmarks = self.web_view.page().profile().bookmarks()
        self.show_table_dialog("Bookmarks", self.bookmarks_table, bookmarks)

    def zoom_in(self):
        self.web_view.setZoomFactor(self.web_view.zoomFactor() + 0.1)

    def zoom_out(self):
        self.web_view.setZoomFactor(self.web_view.zoomFactor() - 0.1)

    def download_file(self):
        # Open a file dialog for downloading files
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.web_view.page().profile().downloadRequested.connect(lambda item: self.handle_download(item, file_name))
            self.web_view.page().profile().download(QUrl(self.web_view.url()))

    def handle_download(self, item, file_name):
        # Handle the download request and save the file
        item.setPath(file_name)
        item.accept()

    def show_table_dialog(self, title, table, data):
        table.setRowCount(data.count())
        for i in range(data.count()):
            item = data.itemAt(i)
            title_item = QTableWidgetItem(item.title())
            url_item = QTableWidgetItem(item.url().toString())

            table.setItem(i, 0, title_item)
            table.setItem(i, 1, url_item)

        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    # Set the initial window state to maximized
    window.setWindowState(window.windowState() | Qt.WindowMaximized)

    window.show()
    sys.exit(app.exec_())
