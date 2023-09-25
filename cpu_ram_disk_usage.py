from tkinter import *
import time
import psutil
from psutil import virtual_memory, cpu_percent, disk_partitions, disk_usage
from tabulate import tabulate
import http.server
import socketserver
import json

# Create a custom request handler
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/cpu":
            cpu_use = cpu_percent(interval=1)
            response = {"CPU Usage": f"{cpu_use}%"}
        elif self.path == "/ram":
            ram_usage = virtual_memory()
            ram_usage = dict(ram_usage._asdict())
            for key in ram_usage:
                if key != 'percent':
                    ram_usage[key] = conversor_bytes_to_gb(ram_usage[key])
            response = {
                "RAM Usage": f"{ram_usage['used']} GB / {ram_usage['total']} GB ({ram_usage['percent']}%)"
            }
        elif self.path == "/disk":
            response = {"Disk Usage": all_disk_info()}
        else:
            # Serve static files (e.g., HTML, CSS)
            super().do_GET()

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

window = Tk()
window.geometry("900x600")
window.title("CPU - RAM- DISK USAGE")

# Function to display CPU information
def show_cpu_info():
    cpu_use = cpu_percent(interval=1)
    cpu_label.config(text=f'{cpu_use}%')
    cpu_label.after(200, show_cpu_info)

# Function to convert Bytes to Gigabytes
def conversor_bytes_to_gb(byte):
    one_gigabyte = 1073741824  # bytes
    giga = byte / one_gigabyte
    giga = '{0:.1f}'.format(giga)
    return giga

# Function to display RAM information
def show_ram_info():
    ram_usage = virtual_memory()
    ram_usage = dict(ram_usage._asdict())
    for key in ram_usage:
        if key != 'percent':
            ram_usage[key] = conversor_bytes_to_gb(ram_usage[key])
    ram_label.config(text=f'{ram_usage["used"]} GB / {ram_usage["total"]} GB ({ram_usage["percent"]}%)')
    ram_label.after(200, show_ram_info)

data = disk_partitions(all=False)

def details(device_name):
    for i in data:
        if i.device == device_name:
            return i

# Function that returns the disk partitions
def get_device_names():
    return [i.device for i in data]  # return C:// D:// E://

# Function to display disk information
def disk_info(device_name):
    disk_info = {}
    try:
        usage = disk_usage(device_name)
        disk_info['Device'] = device_name
        disk_info['Total'] = f"{conversor_bytes_to_gb(usage.total)} GB"
        disk_info['Used'] = f"{conversor_bytes_to_gb(usage.used)} GB"
        disk_info['Free'] = f"{conversor_bytes_to_gb(usage.free)} GB"
        disk_info['Percent'] = f"{usage.percent}%"
    except (PermissionError, FileNotFoundError) as e:
        # Handle exceptions here
        disk_info['Device'] = device_name
        disk_info['Total'] = "N/A"
        disk_info['Used'] = "N/A"
        disk_info['Free'] = "N/A"
        disk_info['Percent'] = "N/A"
    info = details(device_name)
    disk_info.update({"Device": info.device})
    disk_info["Mount Point"] = info.mountpoint
    disk_info["FS-Type"] = info.fstype
    disk_info["Opts"] = info.opts
    return disk_info

# Function to return information of ALL partitions
def all_disk_info():
    return_all = []
    for i in get_device_names():
        return_all.append(disk_info(i))
    return return_all

# Title Program
title_program = Label(window, text='PC Performance Manager', font="arial 40 bold", fg='#14747F')
title_program.place(x=110, y=20)

# CPU title
cpu_title_label = Label(window, text='CPU Usage: ', font="arial 24 bold", fg='#FA5125')
cpu_title_label.place(x=20, y=155)
# Label to show percent of CPU
cpu_label = Label(window, bg='#071C1E', fg='#FA5125', font="Arial 30 bold", width=20)
cpu_label.place(x=230, y=150)

# RAM title
ram_title_label = Label(window, text='RAM Usage: ', font="arial 24 bold", fg='#34A96C')
ram_title_label.place(x=20, y=255)
# Label to show percent of RAM
ram_label = Label(window, bg='#071C1E', fg='#FA5125', font="Arial 30 bold", width=20)
ram_label.place(x=230, y=250)

# Disk title
disk_title_label = Label(window, text='Disk Usage: ', font="arial 24 bold", fg='#797E1E')
disk_title_label.place(x=350, y=360)
# Text area for disk information
textArea = Text(window, bg='#071C1E', fg='yellow', width=85, height=6, padx=10, font=("consolas", 14))
textArea.place(x=15, y=410)

if __name__ == '__main__':
    show_cpu_info()
    show_ram_info()
    info = all_disk_info()
    _list = [i.values() for i in info]
    infoTabulated = tabulate(_list, headers=info[0].keys(), tablefmt="simple", missingval="-")
    textArea.insert(END, infoTabulated)
    window.mainloop()

window.mainloop()

# Create a server instance
PORT = 8000  # Choose an available port
server = socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler)

# Run the server
print(f"Server started on port {PORT}")
server.serve_forever()
