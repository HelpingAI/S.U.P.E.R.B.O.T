import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import tkinter as tk
from tkinter import filedialog, Text

# Function to download images from Google Images
def download_images():
    query = entry1.get()
    num_images = int(entry2.get())

    # Create a directory to store the downloaded images
    if not os.path.exists(query):
        os.makedirs(query)

    # Prepare the Google Images search URL
    base_url = "https://www.google.com/search"
    params = {
        "q": query,
        "tbm": "isch",
        "hl": "en",
        "ijn": "0",
    }

    # Send a GET request to Google Images
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find and download the images
    image_tags = soup.find_all("img")
    for i, img_tag in enumerate(image_tags[:num_images]):
        try:
            img_url = img_tag["src"]
            img_data = requests.get(img_url).content
            with open(os.path.join(query, f"{query}_{i+1}.jpg"), "wb") as img_file:
                img_file.write(img_data)
            print(f"Downloaded {i+1}/{num_images} images")
        except KeyError:
            pass

def quit_program():
    os.system("python SUPERBOT.py")
    root.destroy()

# Create the main window
root = tk.Tk()

# Create the input fields and buttons
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
button1 = tk.Button(root, text="Download Images", command=download_images)
button2 = tk.Button(root, text="Quit", command=quit_program)

# Add the widgets to the window
entry1.pack()
entry2.pack()
button1.pack()
button2.pack()

# Start the main loop
root.mainloop()
