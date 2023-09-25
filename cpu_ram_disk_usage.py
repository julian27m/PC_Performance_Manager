from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import psutil

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data":
            cpu_use = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage("/").percent

            # Create a dictionary to hold the data
            response = {
                "CPUUsage": f"{cpu_use}%",
                "RAMUsage": f"{ram_usage}%",
                "DiskUsage": f"{disk_usage}%"
            }

            # Convert the dictionary to a JSON string
            response_json = json.dumps(response)

            # Send the JSON response
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response_json.encode())
        else:
            # Handle other requests as needed
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not Found".encode())

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
