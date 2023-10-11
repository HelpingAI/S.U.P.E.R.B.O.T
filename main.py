import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
import subprocess
import threading
import queue
from PIL import Image, ImageTk

class TerminalManager:
    def __init__(self, output_callback):
        self.output_callback = output_callback
        self.command_queue = queue.Queue()
        self.process = None

    def start_terminal(self):
        self.process = subprocess.Popen(
            ["cmd.exe"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        threading.Thread(target=self.read_output).start()
        self.process.wait()

    def send_command(self, command):
        if self.process:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()

    def read_output(self):
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            self.output_callback(line)

    def run(self):
        while True:
            command = self.command_queue.get()
            self.send_command(command)

class CustomTerminal(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.mode = tk.StringVar()
        self.mode.set("dark")  # Initial mode is dark
        self.create_widgets()
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(side='top', fill='both', expand=True)

        initial_tab_1 = TerminalFrame(self.tabs, mode=self.mode)
        self.tabs.add(initial_tab_1, text="Tab 1")

        initial_tab_ai = TerminalFrame(self.tabs, script_path="HelpingAI.py", mode=self.mode)
        self.tabs.add(initial_tab_ai, text="HelpingAI")

        new_tab_button = tk.Button(self, text="➕", command=self.create_new_tab, font=('Arial', 10, 'bold'))
        new_tab_button.pack(side='left', padx=5)

        mode_button = tk.Button(self, text="Toggle Mode", command=self.toggle_mode, font=('Arial', 10, 'bold'))
        mode_button.pack(side='right', padx=5)

        real_terminal_thread_1 = threading.Thread(target=initial_tab_1.terminal_manager.run, daemon=True)
        real_terminal_thread_1.start()

        real_terminal_thread_ai = threading.Thread(target=initial_tab_ai.terminal_manager.run, daemon=True)
        real_terminal_thread_ai.start()

        self.tabs.select(initial_tab_1)

    def create_widgets(self):
        pass

    def create_new_tab(self):
        terminal_frame = TerminalFrame(self.tabs, mode=self.mode)
        self.tabs.add(terminal_frame, text=f"Tab {self.tabs.index(tk.END)}")

        close_tab_button = tk.Button(terminal_frame, text="✕", command=lambda: self.close_tab(terminal_frame),
                                     font=('Arial', 10, 'bold'))
        close_tab_button.pack(side='right', padx=5)

        real_terminal_thread = threading.Thread(target=terminal_frame.terminal_manager.run, daemon=True)
        real_terminal_thread.start()

        self.tabs.select(terminal_frame)

    def close_tab(self, tab):
        self.tabs.forget(tab)

    def toggle_mode(self):
        current_mode = self.mode.get()
        new_mode = "light" if current_mode == "dark" else "dark"
        self.mode.set(new_mode)

        for tab_id in self.tabs.tabs():
            tab_frame = self.tabs.nametowidget(tab_id)
            tab_frame.set_mode(new_mode)

class TerminalFrame(tk.Frame):
    def __init__(self, master=None, script_path=None, mode=None, **kwargs):
        super().__init__(master, **kwargs)
        self.mode = mode
        self.create_widgets()
        self.terminal_manager = TerminalManager(self.append_output)
        self.terminal_thread = threading.Thread(target=self.terminal_manager.start_terminal, daemon=True)
        self.terminal_thread.start()

        if script_path:
            self.terminal_manager.command_queue.put(f"python {script_path}")

        self.command_history = []
        self.command_index = 0

    def create_widgets(self):
        bg_color = '#FFFFFF' if self.mode.get() == 'light' else '#1E1E1E'
        fg_color = '#000000' if self.mode.get() == 'light' else '#FFFFFF'

        self.terminal_output = scrolledtext.ScrolledText(self, wrap='word', height=10, width=80, bg=bg_color, fg=fg_color)
        self.terminal_output.pack(side='top', fill='both', expand=True)

        self.terminal_input = tk.Entry(self, width=80, bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.terminal_input.pack(side='bottom', fill='x')
        self.terminal_input.bind("<Return>", self.execute_command)
        self.terminal_input.bind("<Up>", self.navigate_command_history)
        self.terminal_input.bind("<Down>", self.navigate_command_history)

    def execute_command(self, event):
        command = self.terminal_input.get()
        self.terminal_input.delete(0, tk.END)
        self.append_output(f"$ {command}\n")

        self.terminal_manager.command_queue.put(command)

        # Add the command to the history
        if command:
            self.command_history.append(command)
            self.command_index = len(self.command_history)

    def append_output(self, text):
        encoded_text = text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
        self.terminal_output.insert(tk.END, encoded_text)
        self.terminal_output.see(tk.END)

    def navigate_command_history(self, event):
        if event.keysym == "Up":
            if self.command_index > 0:
                self.command_index -= 1
                self.terminal_input.delete(0, tk.END)
                self.terminal_input.insert(tk.END, self.command_history[self.command_index])
        elif event.keysym == "Down":
            if self.command_index < len(self.command_history) - 1:
                self.command_index += 1
                self.terminal_input.delete(0, tk.END)
                self.terminal_input.insert(tk.END, self.command_history[self.command_index])

    def set_mode(self, new_mode):
        self.mode.set(new_mode)
        self.update_colors()

    def update_colors(self):
        bg_color = '#FFFFFF' if self.mode.get() == 'light' else '#1E1E1E'
        fg_color = '#000000' if self.mode.get() == 'light' else '#FFFFFF'

        self.terminal_output.config(bg=bg_color, fg=fg_color)
        self.terminal_input.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Custom Terminal")
    root.configure(bg='#2E2E2E')  # Set the background color

    terminal_frame = CustomTerminal(root, bg='#2E2E2E', bd=1, relief=tk.SUNKEN)
    terminal_frame.pack(side='bottom', fill='both', expand=True)

    root.mainloop()
