import requests
from tkinter import *
from tkinter import ttk

API_URL = "https://api.deezer.com/search"

def get_song_recommendations(query):
    params = {
        "q": query,
        "limit": 50,
        "output": "json",
        "apikey": DEEZER_API_KEY
    }
    
    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("data", [])
        if not tracks:
            return "Sorry, no recommendations found for that query."
        
        recommendations = []
        for i, track in enumerate(tracks):
            recommendations.append(f"{i+1}. {track['title']} by {track['artist']['name']}")
        
        return "\n".join(recommendations)
    else:
        return "Oops! Something went wrong while fetching recommendations."

def open_superbot_file():
    root.destroy()

def fetch_recommendations():
    query = entry.get()
    recommendations = get_song_recommendations(query)
    
    output_text.delete(1.0, END)  # Clear the text area
    output_text.insert(END, recommendations)  # Insert the new text

if __name__ == "__main__":
    root = Tk()
    root.title("Song Recommendations Microbot")
    
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
    
    Label(root, text="Welcome to the Song Recommendations Microbot!", bg='#282a36', fg='white').pack()
    Label(root, text="This microbot can recommend songs based on your query.", bg='#282a36', fg='white').pack()
    
    entry = Entry(root)
    entry.pack()
    
    button_frame = Frame(root, bg='#282a36')
    button_frame.pack(side=BOTTOM)
    
    fetch_button = ttk.Button(button_frame, text="🔍 Fetch Recommendations", command=fetch_recommendations, width=15)
    fetch_button.pack(side=LEFT)
    
    quit_button = ttk.Button(button_frame, text="❌ Quit", command=open_superbot_file, width=15)
    quit_button.pack(side=LEFT)
    
    output_text = Text(root, width=50, height=10)
    output_text.pack()
    
    root.mainloop()
