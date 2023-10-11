import tkinter as tk
from tkinter import ttk, messagebox
import os

class UnitConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Unit Converter")
        master.geometry("400x500")
        master.configure(bg="#3498db")

        self.create_widgets()

    def create_widgets(self):
        # Header Label
        header_label = tk.Label(self.master, text="STANDARD UNIT CONVERTER", font=("Arial", 16), bg="#3498db", fg="#ecf0f1")
        header_label.pack(pady=20)

        # Input Widgets
        input_label = tk.Label(self.master, text="From:", bg="#3498db", fg="#ecf0f1")
        input_label.pack(pady=5)

        self.input_field = ttk.Entry(self.master, background="#ecf0f1")
        self.input_field.pack(pady=5)

        self.input_menu = ttk.Combobox(self.master, values=SELECTIONS, state="readonly")
        self.input_menu.set("Select Unit")
        self.input_menu.pack(pady=10)

        # Output Widgets
        output_label = tk.Label(self.master, text="To:", bg="#3498db", fg="#ecf0f1")
        output_label.pack(pady=5)

        self.output_field = ttk.Entry(self.master, background="#ecf0f1")
        self.output_field.pack(pady=5)

        self.output_menu = ttk.Combobox(self.master, values=SELECTIONS, state="readonly")
        self.output_menu.set("Select Unit")
        self.output_menu.pack(pady=10)

        # Convert and Reset Buttons
        convert_button = tk.Button(self.master, text="CONVERT ✨", bg="#27ae60", fg="#ecf0f1", command=self.convert)
        convert_button.pack(side=tk.BOTTOM, pady=10, padx=5, fill=tk.X)

        reset_button = tk.Button(self.master, text="RESET 🔄", bg="#f39c12", fg="#ecf0f1", command=self.reset)
        reset_button.pack(side=tk.BOTTOM, pady=10, padx=5, fill=tk.X)

        # Quit Button
        quit_button = tk.Button(self.master, text="QUIT 🚀", bg="#c0392b", fg="#ecf0f1", command=self.quit_and_open)
        quit_button.pack(side=tk.BOTTOM, pady=10, padx=5, fill=tk.X)

    def convert(self):
        try:
            input_val = float(self.input_field.get())
            input_unit = self.input_menu.get()
            output_unit = self.output_menu.get()

            # Conversion factors (replace with accurate values)
            conversion_factors = {
                # Length units
                "millimeter": 1,
                "centimeter": 10,
                "meter": 1000,
                "kilometer": 1000000,
                "inch": 25.4,
                "foot": 304.8,
                "mile": 1609344,
                "yard": 914.4,

                # Area units
                "square meter": 1,
                "square kilometer": 1000000,
                "square centimeter": 0.0001,
                "square millimeter": 0.000001,
                "are": 100,
                "hectare": 10000,
                "acre": 4046.856,
                "square mile": 2590000,
                "square foot": 0.0929,

                # Volume units
                "cubic meter": 1000,
                "cubic centimeter": 0.001,
                "litre": 1,
                "millilitre": 0.001,
                "gallon": 3.785,

                # Weight units
                "gram": 1,
                "kilogram": 1000,
                "milligram": 0.001,
                "quintal": 100000,
                "ton": 1000000,
                "pound": 453.592,
                "ounce": 28.3495,

                # Speed units
                "m/s": 1,
                "km/h": 0.277778,
                "mi/h": 0.44704,
            }

            if input_unit in conversion_factors and output_unit in conversion_factors:
                if isinstance(conversion_factors[input_unit], tuple) and isinstance(conversion_factors[output_unit], tuple):
                    # Temperature conversion
                    result = self.convert_temperature(input_val, *conversion_factors[input_unit], *conversion_factors[output_unit])
                else:
                    # Regular unit conversion
                    result = input_val * conversion_factors[input_unit] / conversion_factors[output_unit]

                # Display result in output field
                self.output_field.delete(0, tk.END)
                self.output_field.insert(0, result)

            else:
                messagebox.showerror("Error", "Invalid unit selection")

        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == "celsius" and to_unit == "fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "fahrenheit" and to_unit == "celsius":
            return (value - 32) * (5/9)

    def reset(self):
        self.input_field.delete(0, tk.END)
        self.output_field.delete(0, tk.END)
        self.input_menu.set("Select Unit")
        self.output_menu.set("Select Unit")

    def quit_and_open(self):
        os.system("python SUPERBOT.py")
        self.master.quit()


if __name__ == "__main__":
    SELECTIONS = ["Select Unit", "millimeter", "centimeter", "meter", "kilometer", "foot", "mile", "yard", "inch",
                  "celsius", "fahrenheit", "square meter", "square kilometer", "square centimeter", "square millimeter",
                  "are", "hectare", "acre", "square mile", "square foot", "cubic meter", "cubic centimeter", "litre",
                  "millilitre", "gallon", "gram", "kilogram", "milligram", "quintal", "ton", "pound", "ounce",
                  "m/s", "km/h", "mi/h"]

    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()
os.system("python SUPERBOT.py")