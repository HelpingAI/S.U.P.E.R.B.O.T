import psutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import os
import datetime

class SystemResourcesApp:
    def __init__(self, master):
        self.master = master
        master.title("System Resources Monitor")

        # Create notebook with tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # CPU tab
        self.cpu_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cpu_tab, text='CPU')

        self.cpu_label = tk.Label(self.cpu_tab, text="CPU Usage:")
        self.cpu_label.pack()

        self.cpu_fig, self.cpu_ax = plt.subplots()
        self.cpu_line, = self.cpu_ax.plot([], [], label='CPU Usage')
        self.cpu_ax.set_title('CPU Usage Over Time')
        self.cpu_ax.set_xlabel('Time (s)')
        self.cpu_ax.set_ylabel('CPU Usage (%)')
        self.cpu_ax.legend()

        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.cpu_tab)
        self.cpu_canvas.get_tk_widget().pack()

        self.cpu_ani = animation.FuncAnimation(self.cpu_fig, self.update_cpu_graph, interval=1000)

        # Memory tab
        self.memory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.memory_tab, text='Memory')

        self.memory_label = tk.Label(self.memory_tab, text="Memory Usage:")
        self.memory_label.pack()

        self.memory_fig, self.memory_ax = plt.subplots()
        self.memory_line, = self.memory_ax.plot([], [], label='Memory Usage')
        self.memory_ax.set_title('Memory Usage Over Time')
        self.memory_ax.set_xlabel('Time (s)')
        self.memory_ax.set_ylabel('Memory Usage (%)')
        self.memory_ax.legend()

        self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, master=self.memory_tab)
        self.memory_canvas.get_tk_widget().pack()

        self.memory_ani = animation.FuncAnimation(self.memory_fig, self.update_memory_graph, interval=1000)

        # Disk tab
        self.disk_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.disk_tab, text='Disk')

        self.disk_label = tk.Label(self.disk_tab, text="Disk Usage:")
        self.disk_label.pack()

        self.disk_fig, self.disk_ax = plt.subplots()
        self.disk_line, = self.disk_ax.plot([], [], label='Disk Usage')
        self.disk_ax.set_title('Disk Usage Over Time')
        self.disk_ax.set_xlabel('Time (s)')
        self.disk_ax.set_ylabel('Disk Usage (%)')
        self.disk_ax.legend()

        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, master=self.disk_tab)
        self.disk_canvas.get_tk_widget().pack()

        self.disk_ani = animation.FuncAnimation(self.disk_fig, self.update_disk_graph, interval=1000)

        # Network tab
        self.network_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.network_tab, text='Network')

        self.network_label = tk.Label(self.network_tab, text="Network Sent/Received:")
        self.network_label.pack()

        self.network_fig, self.network_ax = plt.subplots()
        self.sent_line, = self.network_ax.plot([], [], label='Sent')
        self.received_line, = self.network_ax.plot([], [], label='Received')
        self.network_ax.set_title('Network Usage Over Time')
        self.network_ax.set_xlabel('Time (s)')
        self.network_ax.set_ylabel('Network Usage (Bytes)')
        self.network_ax.legend()

        self.network_canvas = FigureCanvasTkAgg(self.network_fig, master=self.network_tab)
        self.network_canvas.get_tk_widget().pack()

        self.network_ani = animation.FuncAnimation(self.network_fig, self.update_network_graph, interval=1000)

        # Summary tab
        self.summary_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_tab, text='Summary')

        self.summary_label = tk.Label(self.summary_tab, text="System Summary:")
        self.summary_label.pack()

        self.system_info_label = tk.Label(self.summary_tab, text="")
        self.system_info_label.pack()

        self.summary_refresh_button = tk.Button(self.summary_tab, text="Refresh Summary", command=self.refresh_summary)
        self.summary_refresh_button.pack()

        # Live system information
        self.live_info_label = tk.Label(master, text="")
        self.live_info_label.pack()

    def update_cpu_graph(self, frame):
        cpu_usage = psutil.cpu_percent(interval=1)
        self.update_graph_data(cpu_usage, self.cpu_line, self.cpu_ax, 'CPU Usage')

        # Update CPU usage label
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")

    def update_memory_graph(self, frame):
        memory = psutil.virtual_memory()
        self.update_graph_data(memory.percent, self.memory_line, self.memory_ax, 'Memory Usage')

        # Update memory usage label
        self.memory_label.config(text=f"Memory Usage: {memory.percent}%")

    def update_disk_graph(self, frame):
        disk_usage = psutil.disk_usage('/')
        self.update_graph_data(disk_usage.percent, self.disk_line, self.disk_ax, 'Disk Usage')

        # Update disk usage label
        self.disk_label.config(text=f"Disk Usage: {disk_usage.percent}%")

    def update_network_graph(self, frame):
        network_stats = psutil.net_io_counters()
        self.update_graph_data(network_stats.bytes_sent, self.sent_line, self.network_ax, 'Sent')
        self.update_graph_data(network_stats.bytes_recv, self.received_line, self.network_ax, 'Received')

        # Update network usage label
        self.network_label.config(text=f"Network Sent: {network_stats.bytes_sent} bytes | Network Received: {network_stats.bytes_recv} bytes")

    def update_graph_data(self, value, line, ax, label):
        # Update graph data for real-time plotting
        x_data, y_data = line.get_data()
        x_data = list(x_data) + [len(x_data)]
        y_data = list(y_data) + [value]
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()

    def refresh_summary(self):
        # Get and display system summary information
        summary_info = f"CPU Usage: {psutil.cpu_percent()}%\n"
        summary_info += f"Memory Usage: {psutil.virtual_memory().percent}%\n"
        summary_info += f"Disk Usage: {psutil.disk_usage('/').percent}%\n"
        summary_info += f"Network Sent: {psutil.net_io_counters().bytes_sent} bytes\n"
        summary_info += f"Network Received: {psutil.net_io_counters().bytes_recv} bytes"

        self.system_info_label.config(text=summary_info)

    def update_live_info(self):
        # Get and display live system information
        live_info = f"CPU: {psutil.cpu_percent()}% | "
        live_info += f"Memory: {psutil.virtual_memory().percent}% | "
        live_info += f"Disk: {psutil.disk_usage('/').percent}% | "
        live_info += f"Sent: {psutil.net_io_counters().bytes_sent} bytes | "
        live_info += f"Received: {psutil.net_io_counters().bytes_recv} bytes | "
        live_info += f"Uptime: {str(datetime.timedelta(seconds=psutil.boot_time()))}"

        self.live_info_label.config(text=live_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemResourcesApp(root)

    # Set up live system information update every second
    app.master.after(1000, app.update_live_info)

    root.mainloop()
