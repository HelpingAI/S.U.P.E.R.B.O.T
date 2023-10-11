import sounddevice
import numpy as np
from scipy.io.wavfile import write
import keyboard
import os
from tkinter import *

def voice_recorder(file_path):
    fs = 44100  # Sampling rate
    seconds = 99999  # Duration of recording

    print("Press 'q' to stop recording...")
    
    recording = []  # Initialize an empty list to store audio data

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    with sounddevice.InputStream(callback=callback, channels=2, samplerate=fs):
        while True:
            if keyboard.is_pressed("q"):  # Check if the 'q' key is pressed
                break

    audio_data = np.concatenate(recording, axis=0)
    write(file_path, fs, audio_data)

    print("Recording Finished")

def start_recording():
    print("Recording Started")
    recording_file = "record.wav"
    voice_recorder(recording_file)

def stop_recording():
    keyboard.press_and_release('q')
    print("Recording Stopped")

def quit_program():
    print("Exiting the program.")
    os.system("python SUPERBOT.py")
    root.destroy()

root = Tk()
root.geometry("200x200")

start_button = Button(root, text="🎤 Start", command=start_recording)
start_button.pack()

stop_button = Button(root, text="⏹️ Stop", command=stop_recording)
stop_button.pack()

quit_button = Button(root, text="❌ Quit", command=quit_program)
quit_button.pack()

root.mainloop()
os.system("python SUPERBOT.py")