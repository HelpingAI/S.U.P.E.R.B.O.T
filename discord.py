import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import webbrowser

class DiscordLinkApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Discord Link App")
        self.master.geometry("400x200")

        self.style = ThemedStyle(self.master)
        self.style.set_theme("equilux")  # You can choose a different theme from the ttkthemes library

        self.label = ttk.Label(master, text="Join Discord for NEW Updates", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.join_discord_button = ttk.Button(master, text="Join Discord", command=self.open_discord_link)
        self.join_discord_button.pack(pady=10)

    def open_discord_link(self):
        discord_link = "https://discord.gg/ZfNPwcutM6"
        webbrowser.open(discord_link)

def main():
    root = tk.Tk()
    app = DiscordLinkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
