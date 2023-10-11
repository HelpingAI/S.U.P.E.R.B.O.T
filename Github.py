import requests
from tkinter import *
from tkinter import ttk, font

API_URL = "https://api.github.com/users/"

def get_github_user(username):
    url = f"{API_URL}{username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_user_repositories(username):
    url = f"{API_URL}{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def open_superbot_file():
    root.destroy()

def fetch_user_data():
    username = entry.get()
    user_data = get_github_user(username)
    
    output_text.delete(1.0, END)  # Clear the text area
    
    if user_data:
        output_text.insert(END, f"Username: {user_data['login']}\n")
        output_text.insert(END, f"Name: {user_data.get('name', 'N/A')}\n")
        output_text.insert(END, f"Location: {user_data.get('location', 'N/A')}\n")
        output_text.insert(END, f"Bio: {user_data.get('bio', 'N/A')}\n\n")
        
        repositories = get_user_repositories(username)
        if repositories:
            output_text.insert(END, "Repositories:\n")
            for repo in repositories:
                output_text.insert(END, f"- {repo['name']}: {repo['description']}\n")
        else:
            output_text.insert(END, "No repositories found.\n")
    else:
        output_text.insert(END, "User not found.\n")

if __name__ == "__main__":
    root = Tk()
    root.title("GitHub User Information Microbot")
    
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
    
    Label(root, text="Welcome to the GitHub User Information Microbot!", bg='#282a36', fg='white').pack(pady=10)
    
    Label(root, text="This microbot retrieves GitHub user information and their repositories.", bg='#282a36', fg='white').pack(pady=10)
    
    entry = Entry(root)
    entry.pack(pady=10)
    
    button_frame = Frame(root, bg='#282a36')
    button_frame.pack(side=BOTTOM, pady=10)
    
    fetch_button = ttk.Button(button_frame, text="🔍 Fetch User Data", command=fetch_user_data, width=20)
    fetch_button.pack(side=LEFT, padx=5)
    
    quit_button = ttk.Button(button_frame, text="❌ Quit", command=open_superbot_file, width=20)
    quit_button.pack(side=LEFT, padx=5)
    
    # Create a scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

     # Create a Text widget with a larger font and attach the scrollbar
    large_font = font.Font(size=14)
    output_text = Text(root, width=50, height=10, yscrollcommand=scrollbar.set, font=large_font)
    output_text.pack(pady=10)

     # Configure the scrollbar to scroll the Text widget
    scrollbar.config(command=output_text.yview)

    
    root.mainloop()
