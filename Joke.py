import sys
import os  # Import the os module for working with file paths
from PyQt5.QtGui import QIcon  # Import QIcon for setting the app icon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextBrowser, QComboBox, QLabel, \
    QMessageBox
import requests
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QTextCursor

class JokeBot(QWidget):
    def __init__(self):
        super().__init__()

        self.last_joke = None

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.output_area = QTextBrowser(self)
        self.output_area.setReadOnly(True)

        self.fetch_button = QPushButton('Fetch Joke', self)
        self.fetch_button.clicked.connect(self.fetch_joke)

        self.save_button = QPushButton('Save Joke', self)
        self.save_button.clicked.connect(self.save_joke)

        self.show_button = QPushButton('Show Saved Jokes', self)
        self.show_button.clicked.connect(self.show_saved_jokes)

        self.delete_button = QPushButton('Delete All Jokes', self)
        self.delete_button.clicked.connect(self.delete_all_jokes)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.quit_program)

        self.category_label = QLabel('Select Category:', self)
        self.category_option = QComboBox(self)
        self.category_option.addItems(['Any', 'Miscellaneous', 'Programming', 'Pun', 'Spooky', 'Christmas'])

        # Set app icon
        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, 'joke.png')  
        self.setWindowIcon(QIcon(icon_path))

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.output_area)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_option)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.show_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.quit_button)

        # Set up the main window
        self.setWindowTitle('Joke Bot')
        self.setGeometry(100, 100, 600, 400)

    def get_joke(self, category='Any'):
        url = f"https://v2.jokeapi.dev/joke/{category}"  # JokeAPI endpoint
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data["type"] == "single":
                self.last_joke = data["joke"]
            elif data["type"] == "twopart":
                self.last_joke = f"{data['setup']}\n{data['delivery']}"
            else:
                self.last_joke = "I couldn't find a joke this time. :("
        else:
            self.last_joke = "Oops! Something went wrong while fetching the joke. :/"

        return self.last_joke

    def fetch_joke(self):
        joke = self.get_joke(category=self.category_option.currentText())
        formatted_joke = self.add_emoji(joke)
        self.append_colored_text(formatted_joke + "\n", QColor('green'))

    def fetch_random_joke(self):
        joke = self.get_joke(category='Any')
        formatted_joke = self.add_emoji(joke)
        self.append_colored_text(formatted_joke + "\n", QColor('green'))

    def add_emoji(self, joke):
        emojis = ["😄", "😃", "😂", "🤣"]
        return f"{emojis[0]} {joke} {emojis[1]}"

    def quit_program(self):
        self.close()

    def save_joke(self):
        if self.last_joke:
            response = QMessageBox.question(self, 'Save Joke', f"Do you want to save this joke?\n\n{self.last_joke}",
                                            QMessageBox.Yes | QMessageBox.No)

            if response == QMessageBox.Yes:
                with open('savedJOKE.txt', 'a') as file:
                    file.write(self.last_joke + "\n\n")
                QMessageBox.information(self, 'Saved!', 'The joke has been saved to \'savedJOKE.txt\'.')

        else:
            QMessageBox.critical(self, 'Error', 'No joke to save.')

    def show_saved_jokes(self):
        try:
            with open('savedJOKE.txt', 'r') as file:
                jokes = file.read()
            QMessageBox.information(self, 'Saved Jokes', jokes)
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', '\'savedJOKE.txt\' not found.')

    def show_favorite_jokes(self):
        if not self.favorite_jokes:
            QMessageBox.information(self, 'No Favorites', 'You haven\'t marked any jokes as favorites.')
        else:
            formatted_favorites = "\n".join(self.favorite_jokes)
            QMessageBox.information(self, 'Favorite Jokes', formatted_favorites)

    def delete_all_jokes(self):
        try:
            with open('savedJOKE.txt', 'w') as file:
                file.write('')
            QMessageBox.information(self, 'Deleted!', 'All saved jokes have been deleted.')
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', '\'savedJOKE.txt\' not found.')

    def copy_to_clipboard(self):
        if self.last_joke:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.last_joke)
            QMessageBox.information(self, 'Copied!', 'The joke has been copied to the clipboard.')
        else:
            QMessageBox.critical(self, 'Error', 'No joke to copy.')

    def append_colored_text(self, text, color):
        cursor = self.output_area.textCursor()
        format = cursor.charFormat()
        format.setForeground(color)
        cursor.setCharFormat(format)
        cursor.insertText(text)
        cursor.movePosition(QTextCursor.End)
        self.output_area.setTextCursor(cursor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    joke_bot = JokeBot()
    joke_bot.show()
    sys.exit(app.exec_())
