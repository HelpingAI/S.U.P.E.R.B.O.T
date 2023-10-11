from pytube import YouTube, Playlist
from moviepy.editor import AudioFileClip
import os
import tkinter as tk
from tkinter import messagebox, filedialog

def download_youtube_video(url, download_audio=True):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        
        status_text.set(f"Downloading: {yt.title} in {stream.resolution}...")
        filename = stream.download()
        status_text.set("Video download completed!")

        if download_audio:
            status_text.set("Converting video to mp3...")
            video_clip = AudioFileClip(filename)
            audio_filename = f"{os.path.splitext(filename)[0]}.mp3"
            video_clip.audio.write_audiofile(audio_filename)
            status_text.set("Audio download completed!")
    
    except Exception as e:
        status_text.set(f"An error occurred: {str(e)}")

def download_youtube_playlist(url, download_audio=True):
    try:
        playlist = Playlist(url)
        
        for video_url in playlist.video_urls:
            download_youtube_video(video_url, download_audio)
    
    except Exception as e:
        status_text.set(f"An error occurred: {str(e)}")

def start_download():
    url = url_entry.get()
    download_audio = var.get()

    if download_audio:
        status_text.set("Coming Soon")
        return

    if "list=" in url:
        download_youtube_playlist(url, download_audio)
    else:
        download_youtube_video(url, download_audio)

    url_entry.delete(0, 'end')

def quit_app():
    os.system("python SUPERBOT.py")
    root.destroy()

root = tk.Tk()
root.title("Youtube video downloader")
root.configure(bg='lightblue')

tk.Label(root, text="Welcome to S.U.P.E.R.B.O.T!", bg='lightblue', font=('Helvetica', 16)).pack(pady=10)

url_label = tk.Label(root, text="YouTube video or playlist URL:", bg='lightblue')
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

var = tk.BooleanVar(value=False)
audio_checkbutton = tk.Checkbutton(root, text="Download audio only", variable=var, bg='lightblue')
audio_checkbutton.pack()

download_button = tk.Button(root, text="Start Download", command=start_download)
download_button.pack(pady=10)

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack(pady=10)

status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text, bg='lightblue')
status_label.pack(pady=10)

root.mainloop()
os.system("python SUPERBOT.py")