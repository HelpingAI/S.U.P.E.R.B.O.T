import sys
import random
import string
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QCheckBox, QPushButton, QTextEdit, QMessageBox, QAction, QFileDialog
from PyQt5.QtGui import QIcon

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Generator")
        self.setWindowIcon(QIcon('pass1.png'))  # Set the window icon
        layout = QVBoxLayout()

        self.label_length = QLabel("Enter desired password length:")
        self.entry_length = QLineEdit()
        self.label_length.setBuddy(self.entry_length)
        layout.addWidget(self.label_length)
        layout.addWidget(self.entry_length)

        self.checkbox_uppercase = QCheckBox("Include Uppercase")
        self.checkbox_lowercase = QCheckBox("Include Lowercase")
        self.checkbox_digits = QCheckBox("Include Digits")
        self.checkbox_special_chars = QCheckBox("Include Special Characters")

        layout.addWidget(self.checkbox_uppercase)
        layout.addWidget(self.checkbox_lowercase)
        layout.addWidget(self.checkbox_digits)
        layout.addWidget(self.checkbox_special_chars)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.button_generate = QPushButton("Generate Password")
        self.button_generate.clicked.connect(self.generate)
        layout.addWidget(self.button_generate)

        self.button_copy = QPushButton("Copy Password")
        self.button_copy.clicked.connect(self.copy_password)
        layout.addWidget(self.button_copy)

        self.button_quit = QPushButton("Quit")
        self.button_quit.clicked.connect(self.quit_program)
        layout.addWidget(self.button_quit)

        self.button_history = QPushButton(f"Password History ({self.get_password_history_count()})")
        self.button_history.clicked.connect(self.show_password_history)
        layout.addWidget(self.button_history)

        self.button_clear_history = QPushButton("Clear History")
        self.button_clear_history.clicked.connect(self.clear_password_history)
        layout.addWidget(self.button_clear_history)

        self.setLayout(layout)

    def generate_password(self, length=12):
        characters = ''
        if self.checkbox_uppercase.isChecked():
            characters += string.ascii_uppercase
        if self.checkbox_lowercase.isChecked():
            characters += string.ascii_lowercase
        if self.checkbox_digits.isChecked():
            characters += string.digits
        if self.checkbox_special_chars.isChecked():
            characters += string.punctuation

        if not characters:
            characters = string.ascii_letters + string.digits + string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def generate(self):
        try:
            password_length = int(self.entry_length.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid integer for password length.")
            return

        generated_password = self.generate_password(password_length)
        strength = self.check_password_strength(generated_password)

        entropy = 2 ** (password_length * 6)
        time_to_break = self.format_time(entropy / (2_000_000_000))
        entropy_formatted = self.format_large_number(entropy)

        self.output.clear()
        self.output.insertPlainText(f"Password: {generated_password}\nStrength: {strength}\nEntropy: {entropy_formatted} combinations\nTime to break: {time_to_break}")

        # Save password to history
        self.save_to_file(generated_password)

        # Update password history button text
        self.button_history.setText(f"Password History ({self.get_password_history_count()})")

    def format_time(self, time_in_seconds):
        if time_in_seconds < 60:
            return f"{time_in_seconds:.2f} seconds"
        elif time_in_seconds < 3600:
            return f"{time_in_seconds / 60:.2f} minutes"
        elif time_in_seconds < 86400:
            return f"{time_in_seconds / 3600:.2f} hours"
        else:
            return f"{time_in_seconds / 86400:.2f} days"

    def format_large_number(self, number):
        suffixes = [' ', 'k', 'M', 'B', 'T']
        index = 0
        while number >= 1000 and index < len(suffixes) - 1:
            number /= 1000
            index += 1
        return f"{number:.2f}{suffixes[index]}"

    def check_password_strength(self, password):
        if any(char.isupper() for char in password) and \
           any(char.islower() for char in password) and \
           any(char.isdigit() for char in password) and \
           any(char in string.punctuation for char in password):
            return "Strong"
        elif len(password) >= 8:
            return "Moderate"
        else:
            return "Weak"

    def save_to_file(self, password):
        try:
            with open('password_history.txt', 'a') as file:
                file.write(password + '\n')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving password to file: {e}")

    def show_password_history(self):
        try:
            with open('password_history.txt', 'r') as file:
                history = file.read()
                QMessageBox.information(self, "Password History", history)
        except FileNotFoundError:
            QMessageBox.information(self, "Password History", "No password history found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading password history: {e}")

    def get_password_history_count(self):
        try:
            with open('password_history.txt', 'r') as file:
                history = file.read()
                return history.count('\n') + 1
        except FileNotFoundError:
            return 0
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading password history: {e}")
            return 0

    def quit_program(self):
        sys.exit()

    def copy_password(self):
        password_start_index = self.output.toPlainText().find('Password: ') + len('Password: ')
        password_end_index = self.output.toPlainText().find('\n', password_start_index)
        password = self.output.toPlainText()[password_start_index:password_end_index]

        clipboard = QApplication.clipboard()
        clipboard.setText(password)

    def clear_password_history(self):
        try:
            with open('password_history.txt', 'w'):
                pass
            self.button_history.setText("Password History (0)")
            QMessageBox.information(self, "Password History", "Password history cleared.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error clearing password history: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())
