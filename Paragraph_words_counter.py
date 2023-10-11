import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class WordCounterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Word Counter App')
        self.setWindowIcon(QIcon('app_icon.png'))  # Add your app icon file

        self.word_entry = QTextEdit(self)
        self.word_entry.setFontPointSize(12)

        self.word_count_label = QLabel(self)
        self.word_count_label.setAlignment(Qt.AlignCenter)
        self.word_count_label.setStyleSheet('font-size: 14pt;')

        self.get_word_count_button = QPushButton('Get Word Count 📝', self)
        self.get_word_count_button.clicked.connect(self.update_word_count)

        self.quit_button = QPushButton('Quit 🚀', self)
        self.quit_button.clicked.connect(self.close_application)

        layout = QVBoxLayout()
        layout.addWidget(self.word_entry)
        layout.addWidget(self.word_count_label)
        layout.addWidget(self.get_word_count_button)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

    def update_word_count(self):
        text = self.word_entry.toPlainText()
        word_count = len(text.split())
        self.word_count_label.setText(f'Word count: {word_count}')

    def close_application(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the app icon here if it's not set in the constructor
    # app_icon = QIcon('app_icon.png')
    # app.setWindowIcon(app_icon)

    main_window = WordCounterApp()
    main_window.show()

    sys.exit(app.exec_())
