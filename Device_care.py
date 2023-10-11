import os
import platform
import shutil
import psutil
from subprocess import run
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory
from threading import Thread

def clean_temp_files():
    try:
        print("Cleaning temporary files...")
        if platform.system().lower() == 'windows':
            run("del /q /s %TEMP%\\*", shell=True)
        else:
            run("rm -rf /tmp/*", shell=True)
        print("Temporary files cleaned successfully.")
    except Exception as e:
        print(f"An error occurred while cleaning temporary files: {e}")
        raise

def check_disk_space():
    try:
        print("Checking disk space...")
        total, used, free = shutil.disk_usage("/")
        message = (
            f"Total disk space: {total} bytes\n"
            f"Used disk space: {used} bytes\n"
            f"Free disk space: {free} bytes"
        )
        print(message)
        messagebox.showinfo("Disk Space", message)
    except Exception as e:
        print(f"An error occurred while checking disk space: {e}")
        raise

def update_software():
    try:
        print("Updating software...")
        if platform.system().lower() == 'windows':
            run("choco upgrade all -y", shell=True)
        else:
            run("sudo apt-get update && sudo apt-get upgrade -y", shell=True)
        print("Software updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating software: {e}")
        raise

def clean_downloads():
    try:
        print("Cleaning Downloads folder...")
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        for file_name in os.listdir(downloads_path):
            file_path = os.path.join(downloads_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        print("Downloads folder cleaned successfully.")
    except Exception as e:
        print(f"An error occurred while cleaning Downloads folder: {e}")
        raise

def find_large_files(directory, size_threshold_mb):
    large_files = []
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if size_mb > size_threshold_mb:
                large_files.append((filepath, size_mb))
    return large_files

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    return {
        'CPU Usage': f"{cpu_usage}%",
        'Memory Usage': f"{memory_info.percent}%",
    }

class DeviceCareApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Device Care App")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        system_tab = ttk.Frame(self.notebook)
        file_tab = ttk.Frame(self.notebook)

        self.notebook.add(system_tab, text="System")
        self.notebook.add(file_tab, text="File")

        # Initialize status_label as an attribute
        self.status_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        # System Tab
        tk.Label(system_tab, text="System Information", font=("Helvetica", 14, "bold")).pack(pady=10)
        self.system_info_label = tk.Label(system_tab, text="", font=("Helvetica", 12))
        self.system_info_label.pack(pady=5)
        tk.Button(system_tab, text="Refresh", command=self.refresh_system_info).pack(pady=5)

        # File Tab
        tk.Label(file_tab, text="File Operations", font=("Helvetica", 14, "bold")).pack(pady=10)
        tk.Button(file_tab, text="Clean Temporary Files", command=self.clean_temp_files_threaded).pack(pady=5)
        tk.Button(file_tab, text="Check Disk Space", command=self.check_disk_space_threaded).pack(pady=5)
        tk.Button(file_tab, text="Update Software", command=self.update_software_threaded).pack(pady=5)
        tk.Button(file_tab, text="Clean Downloads", command=self.clean_downloads_threaded).pack(pady=5)
        tk.Button(file_tab, text="Analyze Large Files", command=self.analyze_large_files).pack(pady=5)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.refresh_system_info()

    def refresh_system_info(self):
        system_info = get_system_info()
        info_text = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
        self.system_info_label.config(text=info_text)

    def clean_temp_files_threaded(self):
        self.run_threaded(clean_temp_files)

    def check_disk_space_threaded(self):
        self.run_threaded(check_disk_space)

    def update_software_threaded(self):
        self.run_threaded(update_software)

    def clean_downloads_threaded(self):
        self.run_threaded(clean_downloads)

    def analyze_large_files(self):
        directory = askdirectory(title="Select Directory to Analyze")
        if directory:
            self.run_threaded(lambda: self.analyze_large_files_threaded(directory))

    def analyze_large_files_threaded(self, directory):
        try:
            large_files = find_large_files(directory, size_threshold_mb=10)
            self.display_large_files(large_files)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
        finally:
            self.progress_bar["value"] = 0

    def display_large_files(self, large_files):
        if not large_files:
            messagebox.showinfo("Large Files Analysis", "No large files found.")
            return

        message = "Large Files:\n\n"
        for filepath, size_mb in large_files:
            message += f"{filepath} - {size_mb:.2f} MB\n"

        print(message)
        messagebox.showinfo("Large Files Analysis", message)

    def run_threaded(self, func):
        self.status_label.config(text="Running...")
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100
        Thread(target=lambda: self.run_operation(func, 0)).start()

    def run_operation(self, func, progress):
        try:
            func()
            self.progress_bar["value"] = 100
            self.status_label.config(text="Operation completed successfully")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
        finally:
            self.progress_bar["value"] = 0

if __name__ == "__main__":
    app = DeviceCareApp()
    app.mainloop()
