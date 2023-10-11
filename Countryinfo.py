import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import subprocess
import webbrowser

def get_country_info(country_name):
    wikipedia_api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": country_name,
        "prop": "extracts|pageimages|info",
        "exintro": True,
        "explaintext": True,
        "piprop": "original",
    }
    response = requests.get(wikipedia_api_url, params=params)
    data = response.json()

    if "query" in data and "pages" in data["query"]:
        page = next(iter(data["query"]["pages"].values()))
        summary = page.get("extract", "No information available on Wikipedia.")
        image_url = page.get("original", {}).get("source")
        return summary, image_url
    else:
        return "No information available on Wikipedia.", None

def get_country_details(country_name):
    restcountries_api_url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(restcountries_api_url)
    data = response.json()

    if isinstance(data, list):
        country_data = data[0]
        languages = ", ".join(country_data["languages"])
        capital = country_data.get("capital", "N/A")
        neighbors = country_data.get("borders", [])
        return languages, capital, neighbors
    else:
        return "N/A", "N/A", []

def on_country_name_click(event):
    country_name = event.widget.get("current linestart", "current lineend").strip()
    wikipedia_summary, _ = get_country_info(country_name)
    messagebox.showinfo("Wikipedia Summary", wikipedia_summary)

def show_country_info():
    country_name = entry.get().strip()
    if not country_name:
        messagebox.showwarning("Warning", "Please enter a country name.")
        return

    wikipedia_summary, image_url = get_country_info(country_name)
    languages, capital, neighbors = get_country_details(country_name)

    text.delete(1.0, tk.END)

    # Add text with different colors
    parts = wikipedia_summary.split('\n')  # Split by newlines for different sections
    for part in parts:
        if "Population" in part:
            text.insert(tk.END, part + '\n', 'green')
        else:
            text.insert(tk.END, part + '\n', 'black')

    text.tag_add("hyperlink", "1.0", "1." + str(len(country_name)))

    # Display country flag if available
    if image_url:
        try:
            image_data = requests.get(image_url).content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((100, 50), Image.ANTIALIAS)
            flag_image = ImageTk.PhotoImage(image)
            text.image_create(tk.END, image=flag_image)
            text.insert(tk.END, '\n\n')
        except Exception as e:
            print(f"Error loading image: {e}")

    # Display additional information
    text.insert(tk.END, f"Official Languages: {languages}\n", 'blue')
    text.insert(tk.END, f"Capital: {capital}\n", 'blue')
    if neighbors:
        text.insert(tk.END, f"Neighboring Countries: {', '.join(neighbors)}\n", 'blue')

def show_location_on_map():
    country_name = entry.get().strip()
    if not country_name:
        messagebox.showwarning("Warning", "Please enter a country name.")
        return

    try:
        subprocess.run(["python", "Google_maps.py", country_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Google_maps.py: {e}")

def clear_text():
    text.delete(1.0, tk.END)

def save_to_file():
    country_info = text.get("1.0", tk.END)
    with open("country_info.txt", "w") as file:
        file.write(country_info)

def open_wikipedia_page():
    country_name = entry.get().strip()
    if not country_name:
        messagebox.showwarning("Warning", "Please enter a country name.")
        return
    webbrowser.open(f"https://en.wikipedia.org/wiki/{country_name}")

def quit_program():
    root.destroy()

root = tk.Tk()
root.title("Country Info Bot")
root.configure(bg='light blue')

# Define text color tags
text = tk.Text(root)
text.tag_configure('green', foreground='green')
text.tag_configure('black', foreground='black')
text.tag_configure('blue', foreground='blue')

title_label = tk.Label(root, text="Country Info Bot", font=("Helvetica", 16), bg='light blue')
title_label.pack(side='top', pady=10)

entry_label = tk.Label(root, text="Enter country name:", bg='light blue')
entry_label.pack(side='top')

entry = tk.Entry(root)
entry.pack(side='top', fill='x')

text_scrollbar = tk.Scrollbar(root)
text_scrollbar.pack(side='right', fill='y')

text = tk.Text(root, yscrollcommand=text_scrollbar.set)
text.pack(fill='both', expand=True)

text_scrollbar.config(command=text.yview)

button_frame = tk.Frame(root, bg='light blue')
button_frame.pack(side='bottom', fill='x')

info_button = tk.Button(button_frame, text="🌍 Get Info", command=show_country_info)
info_button.pack(side='left')

location_button = tk.Button(button_frame, text="🗺️ Show on Map", command=show_location_on_map)
location_button.pack(side='left')

clear_button = tk.Button(button_frame, text="Clear", command=clear_text)
clear_button.pack(side='left')

save_button = tk.Button(button_frame, text="Save to File", command=save_to_file)
save_button.pack(side='left')

open_wiki_button = tk.Button(button_frame, text="Open Wikipedia Page", command=open_wikipedia_page)
open_wiki_button.pack(side='left')

quit_button = tk.Button(button_frame, text="❌ Quit", command=quit_program)
quit_button.pack(side='left')

text.tag_bind("hyperlink", "<Button-1>", on_country_name_click)

root.mainloop()
