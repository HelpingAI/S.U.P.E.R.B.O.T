import sys
import requests
import geocoder
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QTextBrowser, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QInputDialog, QRadioButton, QButtonGroup
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Weather App')
        self.setWindowIcon(QIcon('weather.png'))  # Set the app icon

        # Unit selection
        self.unit_label = QLabel('Select Unit:')
        self.unit_combobox = QComboBox()
        self.unit_combobox.addItems(['Celsius', 'Fahrenheit'])
        self.unit_combobox.setCurrentIndex(0)

        # Forecast period
        self.forecast_label = QLabel('Forecast Period (hours):')
        self.forecast_entry = QLineEdit('24')

        # Output area
        self.output_area = QTextBrowser()

        # Use current location checkbox
        self.location_checkbox = QCheckBox('Use Current Location')

        # Weather duration selection
        self.weather_duration_label = QLabel('Select Weather Duration:')
        self.current_weather_radio = QRadioButton('Current Weather')
        self.two_day_forecast_radio = QRadioButton('2-Day Forecast')

        # Button group for radio buttons
        self.weather_duration_group = QButtonGroup(self)
        self.weather_duration_group.addButton(self.current_weather_radio, 0)
        self.weather_duration_group.addButton(self.two_day_forecast_radio, 1)
        self.weather_duration_group.buttonClicked.connect(self.weather_duration_changed)

        # Buttons
        self.fetch_button = QPushButton('Fetch Weather')
        self.clear_button = QPushButton('Clear')
        self.quit_button = QPushButton('Quit')

        # Layout setup
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.unit_label)
        v_layout.addWidget(self.unit_combobox)
        v_layout.addWidget(self.forecast_label)
        v_layout.addWidget(self.forecast_entry)
        v_layout.addWidget(self.output_area)
        v_layout.addWidget(self.location_checkbox)

        h_duration_layout = QHBoxLayout()
        h_duration_layout.addWidget(self.weather_duration_label)
        h_duration_layout.addWidget(self.current_weather_radio)
        h_duration_layout.addWidget(self.two_day_forecast_radio)

        v_layout.addLayout(h_duration_layout)

        h_button_layout = QHBoxLayout()
        h_button_layout.addWidget(self.fetch_button)
        h_button_layout.addWidget(self.clear_button)
        h_button_layout.addWidget(self.quit_button)

        v_layout.addLayout(h_button_layout)

        self.setLayout(v_layout)

        # Button connections
        self.fetch_button.clicked.connect(self.fetch_weather)
        self.clear_button.clicked.connect(self.clear_output)
        self.quit_button.clicked.connect(self.close)

        # Check for API key on startup
        self.get_api_key()

    def weather_duration_changed(self, button):
        if button.text() == 'Current Weather':
            self.forecast_label.setDisabled(True)
            self.forecast_entry.setDisabled(True)
        elif button.text() == '2-Day Forecast':
            self.forecast_label.setDisabled(False)
            self.forecast_entry.setDisabled(False)

    def fetch_weather(self):
        API_KEY = self.get_api_key()

        if not API_KEY:
            return  # User canceled or closed the dialog

        UNIT = self.unit_combobox.currentText()

        if self.location_checkbox.isChecked():
            coordinates = self.get_location_coordinates()
            if coordinates:
                weather_data = self.get_weather_data(API_KEY, coordinates)
                weather_duration = self.weather_duration_group.checkedId()
                formatted_data = self.format_weather_data(weather_data, UNIT, weather_duration)
            else:
                formatted_data = "Failed to get location coordinates."
        else:
            formatted_data = "City name not provided."

        self.output_area.clear()
        self.output_area.append(formatted_data)

    def clear_output(self):
        self.output_area.clear()

    def get_location_coordinates(self):
        try:
            location = geocoder.ip('me').latlng
            return location
        except Exception as e:
            self.output_area.append(f"Failed to get location coordinates. Error: {str(e)}")
            return None

    def get_weather_data(self, api_key, location):
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": location[0],
            "lon": location[1],
            "appid": api_key,
            "units": "metric",
            "cnt": int(self.forecast_entry.text()) if self.two_day_forecast_radio.isChecked() else 1
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": f"Failed to fetch weather data. Status code: {response.status_code}"}

    def convert_temperature(self, temperature, to_unit):
        if to_unit.lower() == 'fahrenheit':
            return (temperature * 9/5) + 32
        elif to_unit.lower() == 'celsius':
            return temperature
        else:
            raise ValueError("Invalid unit")

    def temperature_trend(self, current_temp, previous_temp):
        if current_temp > previous_temp:
            return "📈 Rising"
        elif current_temp < previous_temp:
            return "📉 Falling"
        else:
            return "📊 Stable"

    def get_weather_icon(self, weather_description):
        weather_icons = {
            "clear sky": "☀️",
            "few clouds": "🌤️",
            "scattered clouds": "🌥️",
            "broken clouds": "☁️",
            "shower rain": "🌦️",
            "rain": "🌧️",
            "thunderstorm": "⛈️",
            "snow": "❄️",
            "mist": "🌫️"
        }

        return weather_icons.get(weather_description.lower(), "❓")

    def format_weather_data(self, weather_data, unit, weather_duration):
        try:
            current_weather = weather_data["list"][0]

            if weather_duration == 0:  # Current Weather
                description = current_weather["weather"][0]["description"] if current_weather["weather"] else "Not Available"
                temperature = self.convert_temperature(current_weather["main"]["temp"], unit)
                wind_speed = current_weather["wind"]["speed"] if current_weather["wind"] else "Not Available"
                wind_direction = current_weather["wind"]["deg"] if current_weather["wind"] else "Not Available"
                humidity = current_weather["main"]["humidity"] if current_weather["main"] else "Not Available"
                pressure = current_weather["main"]["pressure"] if current_weather["main"] else "Not Available"
                uv_index = current_weather.get("uv", 0)

                formatted_data = f"🌦️ **Current Weather** 🌦️\n"\
                                 f"🌡️ Temperature: {temperature:.2f}°{unit[0]}  {self.temperature_trend(temperature, 0)}\n"\
                                 f"💨 Wind Speed: {wind_speed} m/s\n"\
                                 f"🧭 Wind Direction: {wind_direction}°\n"\
                                 f"💧 Humidity: {humidity}%\n"\
                                 f"🌫️ Pressure: {pressure} hPa\n"\
                                 f"☀️ UV Index: {uv_index}\n"\
                                 f"🌈 Description: {description} {self.get_weather_icon(description)}\n"

            else:  # 2-Day Forecast
                future_weather = weather_data["list"][1:]

                formatted_data = f"🌦️ **{int(self.forecast_entry.text())}-Hour Forecast** 🌦️\n"

                for i, forecast in enumerate(future_weather):
                    temp_min = forecast["main"]["temp_min"] if forecast["main"] else "Not Available"
                    temp_max = forecast["main"]["temp_max"] if forecast["main"] else "Not Available"
                    description = forecast["weather"][0]["description"] if forecast["weather"] else "Not Available"
                    temp_min = self.convert_temperature(temp_min, unit)
                    temp_max = self.convert_temperature(temp_max, unit)

                    formatted_data += f"{i * 3} hours from now:\n"\
                                      f"🌡️ Temperature: {temp_min:.2f}°{unit[0]} - {temp_max:.2f}°{unit[0]}\n"\
                                      f"🌈 Description: {description} {self.get_weather_icon(description)}\n\n"

            return formatted_data

        except KeyError:
            return "Invalid or incomplete weather data."

    def get_api_key(self):
        try:
            with open('OpenweatherAPI.txt', 'r') as file:
                api_key = file.read().strip()  # Remove leading/trailing whitespaces
        except FileNotFoundError:
            api_key = None

        # Ask for the API key if not found or empty
        while not api_key:
            result, ok = QInputDialog.getText(self, 'Input', 'Enter your OpenWeatherMap API key:', QLineEdit.Password)
            
            if not ok:
                # User pressed Cancel or closed the dialog
                self.close()

            api_key = result.strip()

            with open('OpenweatherAPI.txt', 'w') as file:
                file.write(api_key)

        return api_key

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
