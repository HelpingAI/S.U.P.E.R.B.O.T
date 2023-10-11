import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
import requests

class MovieRecommendationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.API_URL = "https://api.themoviedb.org/3/search/movie"
        self.api_key_filename = "TMDBapi.txt"
        self.api_key = self.get_api_key()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Movie Recommendation Microbot')
        self.setWindowIcon(QIcon('mov.png'))  # 

        layout = QVBoxLayout()

        label = QLabel('Enter a topic for movie recommendations:')
        self.entry = QLineEdit()
        text = QTextEdit()
        text.setReadOnly(True)

        get_button = QPushButton('🎬 Get Recommendations', self)
        get_button.clicked.connect(self.show_recommendations)

        omdb_button = QPushButton('🌐 OMDb', self)
        omdb_button.clicked.connect(self.open_omdb)

        quit_button = QPushButton('❌ Quit', self)
        quit_button.clicked.connect(self.quit_program)

        layout.addWidget(label)
        layout.addWidget(self.entry)
        layout.addWidget(text)
        layout.addWidget(get_button)
        layout.addWidget(omdb_button)
        layout.addWidget(quit_button)

        self.setLayout(layout)

        self.show()

    def get_api_key(self):
        try:
            with open(self.api_key_filename, "r") as file:
                api_key = file.read().strip()
                if not api_key:
                    raise FileNotFoundError
                return api_key
        except FileNotFoundError:
            api_key, _ = QFileDialog.getOpenFileName(self, 'Select your TMDb API key file')
            if api_key:
                self.save_api_key(api_key)
                return api_key
            else:
                sys.exit()

    def save_api_key(self, api_key):
        with open(self.api_key_filename, "w") as file:
            file.write(api_key)

    def get_movie_recommendations(self, topic):
        params = {
            "api_key": self.api_key,
            "query": topic,
            "language": "en-US",
            "page": 1,
            "region": "IN"
        }

        response = requests.get(self.API_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            movies = data.get("results", [])

            if not movies:
                return "No movies found on this topic."

            recommendations = [movie.get("title", "Unknown Title") for movie in movies]
            return recommendations
        else:
            return "Oops! Something went wrong while fetching movie recommendations."

    def show_recommendations(self):
        topic = self.entry.text()
        recommendations = self.get_movie_recommendations(topic)

        if isinstance(recommendations, list):
            QMessageBox.information(self, "Recommendations", "\n".join(recommendations))
        else:
            QMessageBox.critical(self, "Error", recommendations)

    def quit_program(self):
        sys.exit()

    def open_omdb(self):
        QMessageBox.information(self, "Information", "This feature will be available soon.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MovieRecommendationApp()
    sys.exit(app.exec_())
