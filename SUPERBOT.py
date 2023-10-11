import os
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from time import strftime
import pyautogui
import time

# Updated - a dictionary to store user credentials
user_credentials = {}

# Updated - File path to store user credentials
credentials_file_path = "user_credentials.txt"
def save_credentials_to_file():
    with open(credentials_file_path, "w") as file:
        for username, password in user_credentials.items():
            file.write(f"{username} {password}\n")
def load_credentials_from_file():
    try:
        with open(credentials_file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                username, password = line.strip().split()
                user_credentials[username] = password
    except FileNotFoundError:
        pass  # Ignore if the file doesn't exist
load_credentials_from_file()

def open_super_terminal():
    if authenticated:
        os.system("python main.py")
    else:
        messagebox.showinfo("Authentication Required", "Please login to use S.U.P.E.R.B.O.T.")



def create_command_buttons(frame, commands):
    buttons = []
    for command in commands:
        if command in ["Gym", "Password_Cracker", "Snake_Game", "KBC_quiz_game", "SuperSurfer_Web_Browser"]:
            button = tk.Button(frame, text=command, command=lambda cmd=command: run_command(cmd), bg='#FF0000', fg='white',
                               relief='raised', bd=5, font=("Helvetica", 10, 'bold'))
        else:
            button = tk.Button(frame, text=command, command=lambda cmd=command: run_command(cmd), bg='#98FB98', fg='#2F4F4F',
                               relief='raised', bd=5, font=("Helvetica", 10, 'bold'))
        buttons.append(button)
        button.bind("<Enter>", lambda event, btn=button: on_enter(event, btn))
        button.bind("<Leave>", lambda event, btn=button: on_leave(event, btn))
    return buttons

def run_command(command):
    # Updated - Check if the user is authenticated
    if not authenticated:
        messagebox.showwarning("Authentication Required", "Please login to use S.U.P.E.R.B.O.T.")
        return

    if command in ["Gym", "Password_Cracker", "Snake_Game", "KBC_quiz_game", "SuperSurfer__Web_Browser"]:
        messagebox.showinfo("Coming Soon", "This feature is coming soon!")
    else:
        os.system(f"python {command}.py")


def display_realtime_output():
    time_string = strftime('%A %H:%M:%S %p')  # Added day to the time
    realtime_label.config(text=time_string)
    root.after(1000, display_realtime_output)  # Update every second

def on_enter(event, button):
    button.config(font=("Helvetica", 10, 'bold underline'), fg='#00ff00')  # Add a refined glow effect on hover

def on_leave(event, button):
    button.config(font=("Helvetica", 10, 'bold'), fg='black')  # Remove the glow effect on leave

def create_command_notebook():
    notebook = ttk.Notebook(root)

    # List of commands for each page
    commands = [
        "News", "Weather", "Joke", "Motivation", "Wolframalpha", "Movierecomender", "PasswordGenerator",
        "Facts", "Searchbook", "Stacksoverflow", "Github", "SearchSongs", "CalculateAge", "Google_MAPs", "Google",
        "HelpingAI", "Timetable", "Countryinfo", "Wikipedia", "Dictionary", "Paragraph_words_counter", "Password_Cracker",
        "Restaurant_Management_System", "Student_Management_System", "Puzzle_Game", "Snake_Game", "KBC_quiz_game",
        "Text_to_Speech", "Notepad", "Gym", "File_manager", "Drawing_Application", "Spelling_Checker", "TO-Do_list",
        "Typing_speed_test", "Calculator", "SuperSurfer_Web_Browser", "Voice_Recorder", "Translator", "Youtube_Downloader",
        "Audio_Player", "Download_Image", "Subway_Surfer", "Rabbit_run", "Chess", "Units_converter", "Screen_recorder",
        "Alarm", "ChatGPT", "H20_GPT", "background_remover", "Camera", "Timer", "Media_Player", "Ping_Pong", "Device_care",
        "cargame", "Spellingbee", "System_Resource_Monitor"
    ]

    # Number of buttons per page
    buttons_per_page = 8

    # Calculate the number of pages needed
    num_pages = -(-len(commands) // buttons_per_page)  # Ceiling division

    for page_num in range(num_pages):
        start_index = page_num * buttons_per_page
        end_index = (page_num + 1) * buttons_per_page
        page_commands = commands[start_index:end_index]

        frame = tk.Frame(notebook, bg='#87CEEB')  # You can customize the background color
        notebook.add(frame, text=f'Page {page_num + 1}')

        buttons = create_command_buttons(frame, page_commands)
        for button in buttons:
            button.pack(anchor='w', fill='x')

    return notebook
def open_app_from_pc():
    try:
        application_name = simpledialog.askstring("Open App", "Enter the application name:")
        if application_name:
            pyautogui.hotkey('win')
            time.sleep(1)
            pyautogui.write(application_name)
            pyautogui.press('enter')
            status_label.config(text=f"Opening {application_name}...", fg="#0000ff")
    except Exception as e:
        print(f"An error occurred: {e}")

def open_discord_updates():
    os.system("python discord.py")

def load_content_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except UnicodeDecodeError as e:
        return f"Error decoding file: {e}"

# Updated - Function to sign up a new user
def sign_up():
    username = simpledialog.askstring("Sign Up", "Enter your username:")
    password = simpledialog.askstring("Sign Up", "Enter your password:")

    # Updated - Save the credentials
    user_credentials[username] = password
    save_credentials_to_file()
    messagebox.showinfo("Sign Up", "Sign Up successful!")
    
def destroy_apis_file():
    try:
        directory = os.getcwd()
        files = os.listdir(directory)
        for file in files:
            if 'API' in file or 'api' in file:
                os.remove(os.path.join(directory, file))
        status_label.config(text="API files destroyed.", fg="#FF0000")
    except Exception as e:
        print(f"An error occurred: {e}")

authenticated = False

def authenticate_user():
    # Updated - Check if the user is already authenticated
    global authenticated
    if authenticated:
        return

    username = simpledialog.askstring("Login", "Enter your username:")
    password = simpledialog.askstring("Login", "Enter your password:")

    # Updated - Check if the username is in the dictionary
    if username in user_credentials:
        # Updated - Check if the entered password matches the stored password
        if password == user_credentials[username]:
            messagebox.showinfo("Authentication", "Login successful!")
            authenticated = True
            # Perform actions for authenticated users here
        else:
            messagebox.showerror("Authentication Error", "Invalid password.")
    else:
        messagebox.showerror("Authentication Error", "Invalid username. Please sign up if you haven't already.")


# Main Tkinter window
root = tk.Tk()
root.title("S.U.P.E.R.B.O.T.")  # Change the title of the app


# Real-time label
realtime_label = tk.Label(root, text="", font=("Helvetica", 12, 'bold'), fg='#00ff00')  # LimeGreen
realtime_label.pack(side='top', padx=10, pady=10)

# Authentication button
auth_button = tk.Button(root, text="Authenticate", command=authenticate_user, bg='#8B4513', fg='white',
                        relief='raised', bd=5, font=("Helvetica", 10, 'bold'))
auth_button.pack(side='top', pady=10)
auth_button.bind("<Enter>", lambda event: on_enter(event, auth_button))
auth_button.bind("<Leave>", lambda event: on_leave(event, auth_button))

# Sign Up button
sign_up_button = tk.Button(root, text="Sign Up", command=sign_up, bg='#8B4513', fg='white',
                        relief='raised', bd=5, font=("Helvetica", 10, 'bold'))
sign_up_button.pack(side='top', pady=10)
sign_up_button.bind("<Enter>", lambda event: on_enter(event, sign_up_button))
sign_up_button.bind("<Leave>", lambda event: on_leave(event, sign_up_button))

# Super Terminal button
super_terminal_button = tk.Button(root, text="Super Terminal", command=open_super_terminal, bg='#800080', fg='white',
                                  relief='raised', bd=5, font=("Helvetica", 10, 'bold'))
super_terminal_button.pack(side='top', pady=10)
super_terminal_button.bind("<Enter>", lambda event: on_enter(event, super_terminal_button))
super_terminal_button.bind("<Leave>", lambda event: on_leave(event, super_terminal_button))

# Open App button
open_app_button = tk.Button(root, text="Open App from PC", command=open_app_from_pc, bg='#FFA500', fg='#000000',
                            relief='raised', bd=5, font=("Helvetica", 10, 'bold'))
open_app_button.pack(side='top', pady=10)

# Updates button
updates_button = tk.Button(root, text="Updates", command=open_discord_updates, bg='#FFFF00', fg='#000000',
                            relief='raised', bd=5, font=("Helvetica", 10, 'bold'))
updates_button.pack(side='top', pady=10)
updates_button.bind("<Enter>", lambda event: on_enter(event, updates_button))
updates_button.bind("<Leave>", lambda event: on_leave(event, updates_button))

# Destroy APIs button
destroy_apis_button = tk.Button(root, text="Destroy APIs", command=destroy_apis_file, bg='#FF0000', fg='white',
                                relief='raised', bd=5, font=("Helvetica", 10, 'bold'))
destroy_apis_button.pack(side='top', pady=10)
destroy_apis_button.bind("<Enter>", lambda event: on_enter(event, destroy_apis_button))
destroy_apis_button.bind("<Leave>", lambda event: on_leave(event, destroy_apis_button))

# Create and pack notebook with buttons
command_notebook = create_command_notebook()
command_notebook.pack(side='top', padx=10, pady=10)

# Start displaying real-time updates
display_realtime_output()

# Status label
status_label = tk.Label(root, text="", font=("Helvetica", 12, 'bold'), fg='#0000ff')  # Blue
status_label.pack(side='bottom', padx=10, pady=10)

root.mainloop()
