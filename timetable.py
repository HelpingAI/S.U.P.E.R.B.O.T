import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QFormLayout
from PyQt5.QtGui import QIcon
import pickle

class TimeTableApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Time Table Microbot")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon("your_icon_file.png"))  # Replace with your icon file

        # Load the time table data
        self.time_table = self.load_time_table()

        self.init_ui()

    def init_ui(self):
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)

        self.day_label = QLabel("Day:")
        self.day_entry = QLineEdit()

        self.subject_label = QLabel("Subject:")
        self.subject_entry = QLineEdit()

        self.display_button = QPushButton("Display Time Table")
        self.add_button = QPushButton("Add Subject")
        self.remove_button = QPushButton("Remove Subject")
        self.save_button = QPushButton("Save Time Table")
        self.quit_button = QPushButton("Quit")

        layout = QVBoxLayout()
        layout.addWidget(self.output_area)

        form_layout = QFormLayout()
        form_layout.addRow(self.day_label, self.day_entry)
        form_layout.addRow(self.subject_label, self.subject_entry)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.display_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.quit_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect buttons to functions
        self.display_button.clicked.connect(self.display_time_table)
        self.add_button.clicked.connect(self.add_subject)
        self.remove_button.clicked.connect(self.remove_subject)
        self.save_button.clicked.connect(self.save_time_table)
        self.quit_button.clicked.connect(self.close)

        # Display the time table initially
        self.display_time_table()

    def display_time_table(self):
        text = self._display_time_table(self.time_table)
        self.update_output(text)

    def add_subject(self):
        text = self._add_subject(self.time_table, self.day_entry.text(), self.subject_entry.text())
        self.update_output(text)

    def remove_subject(self):
        text = self._remove_subject(self.time_table, self.day_entry.text(), self.subject_entry.text())
        self.update_output(text)

    def update_output(self, text):
        self.output_area.setPlainText(text)

    def save_time_table(self):
        save_dialog = QFileDialog()
        file_name, _ = save_dialog.getSaveFileName(self, 'Save Time Table', '', 'Pickle Files (*.pickle);;All Files (*)')

        if file_name:
            with open(file_name, "wb") as file:
                pickle.dump(self.time_table, file)

    def load_time_table(self):
        try:
            with open("time_table.pickle", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def _display_time_table(self, time_table):
        if not time_table:
            return "Your time table is currently empty."
        else:
            output = "Your Current Time Table:\n"
            for day, subjects in time_table.items():
                output += f"{day}: {', '.join(subjects)}\n"
            return output

    def _add_subject(self, time_table, day, subject):
        if day in time_table:
            time_table[day].append(subject)
        else:
            time_table[day] = [subject]
        return f"Added {subject} to {day}."

    def _remove_subject(self, time_table, day, subject):
        if day in time_table and subject in time_table[day]:
            time_table[day].remove(subject)
            return f"Removed {subject} from {day}."
        else:
            return f"{subject} not found in {day}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TimeTableApp()
    ex.show()
    sys.exit(app.exec_())
