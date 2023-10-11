from datetime import datetime
from tkinter import *
from tkinter import ttk, font
from tkcalendar import DateEntry  # Import the DateEntry widget

def calculate_age(birth_date):
    current_date = datetime.now()
    age = current_date - birth_date
    years = age.days // 365
    months = (age.days % 365) // 30
    days = (age.days % 365) % 30
    hours = age.seconds // 3600
    return years, months, days, hours

def open_superbot_file():
    root.destroy()

def fetch_age():
    input_date = entry.get_date()  # Get the selected date
    
    try:
        birth_date = datetime.strptime(str(input_date), "%Y-%m-%d")
        age_years, age_months, age_days, age_hours = calculate_age(birth_date)
        
        output_text.delete(1.0, END)  # Clear the text area
        output_text.insert(END, f"You are {age_years} years, {age_months} months, {age_days} days, and {age_hours} hours old.\n")
    except ValueError:
        output_text.delete(1.0, END)  # Clear the text area
        output_text.insert(END, "Invalid input. Please enter your birthdate in the YYYY-MM-DD format.\n")

if __name__ == "__main__":
    root = Tk()
    root.title("Age Calculator Microbot")
    
    # Set background color for the window
    root.configure(bg='#282a36')
    
    style = ttk.Style()
    style.configure("TButton",
                    foreground="black",
                    background="#50fa7b",
                    font=("Arial", 20),
                    padding=10)
    
    style.map("TButton",
              foreground=[('pressed', 'red'), ('active', 'blue')],
              background=[('pressed', '!disabled', 'black'), ('active', 'white')])
    
    Label(root, text="Welcome to the Age Calculator Microbot!", bg='#282a36', fg='white').pack(pady=10)
    
    Label(root, text="This microbot calculates your age based on your birthdate.", bg='#282a36', fg='white').pack(pady=10)
    
    entry = DateEntry(root)  # Use DateEntry instead of Entry
    entry.pack(pady=10)
    
    button_frame = Frame(root, bg='#282a36')
    button_frame.pack(side=BOTTOM, pady=10)
    
    fetch_button = ttk.Button(button_frame, text="🔍 Calculate Age", command=fetch_age, width=20)
    fetch_button.pack(side=LEFT, padx=5)
    
    quit_button = ttk.Button(button_frame, text="❌ Quit", command=open_superbot_file, width=20)
    quit_button.pack(side=LEFT, padx=5)
    
     # Create a Text widget with a larger font and attach the scrollbar
    large_font = font.Font(size=14)
    output_text = Text(root, width=50, height=10, font=large_font)
    output_text.pack(pady=10)

    
    root.mainloop()
