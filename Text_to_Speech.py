import pyttsx3
import os
from tkinter import *

# Initializing the module
engine = pyttsx3.init()

def speak():
    # Using .say() function to speak the user's input
    engine.say(entry.get())

    # Processing and running the program commands
    engine.runAndWait()

def quit_program():
    print("Exiting the program.")
    os.system("python SUPERBOT.py")
    root.destroy()

# Create a GUI window
root = Tk()
root.title("Text-to-Speech Program")
root.geometry("300x200")

# Create an Entry widget for user to type their message
entry = Entry(root, width=30)
entry.pack(pady=20)

# Create a Button widget to trigger the speak function
speak_button = Button(root, text="Speak", command=speak)
speak_button.pack(pady=10)

# Create a Button widget to quit the program
quit_button = Button(root, text="Quit", command=quit_program)
quit_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()
os.system("python SUPERBOT.py")