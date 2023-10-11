from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Alarm")
        self.setWindowIcon(QIcon("Alarm.png"))  # Set the window icon
        self.central_widget = QWebEngineView()
        self.setCentralWidget(self.central_widget)
        self.central_widget.load(QUrl("https://vclock.com/"))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
try:
    sys.exit(app.exec_())
except SystemExit:
    pass