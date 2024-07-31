import psutil
import time
from datetime import datetime
import tkinter as tk
import os
import json

class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Usage Monitor")

        # Set window attributes
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'white')  # Set transparency color
        self.root.geometry("+1300+0")  # Adjust position to top right corner

        self.data_file = "network_data.json"
        self.load_data()

        self.sent_start, self.recv_start = self.get_network_usage()

        self.setup_gui()
        self.update_network_usage()

    def get_network_usage(self):
        net_io = psutil.net_io_counters()
        return net_io.bytes_sent, net_io.bytes_recv

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.total_sent = data.get("total_sent", 0)
                self.total_recv = data.get("total_recv", 0)
        else:
            self.total_sent = 0
            self.total_recv = 0

    def save_data(self):
        data = {
            "total_sent": self.total_sent,
            "total_recv": self.total_recv
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file)

    def setup_gui(self):
        # Configure the label for network usage display
        self.label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="#1bfc06", bg="white")
        self.label.pack(padx=10, pady=5)

        # Add close button with a smaller size
        self.close_button = tk.Button(self.root, text="X", command=self.root.quit, bg="white", fg="red", font=("Helvetica", 8), bd=0)
        self.close_button.place(relx=1.0, rely=0.0, anchor='ne')  # Position at the top right corner

    def update_network_usage(self):
        sent_now, recv_now = self.get_network_usage()

        sent = sent_now - self.sent_start
        recv = recv_now - self.recv_start

        self.total_sent += sent
        self.total_recv += recv

        self.label.config(text=f"D: {self.total_recv / (1024 ** 2):.2f} MB, U: {self.total_sent / (1024 ** 2):.2f} MB")

        self.sent_start, self.recv_start = sent_now, recv_now
        self.save_data()

        self.root.after(1000, self.update_network_usage)  # Update every second

if __name__ == "__main__":
    root = tk.Tk()
    root.config(bg="white")  # Set background color to match transparency
    app = NetworkMonitor(root)
    root.mainloop()
