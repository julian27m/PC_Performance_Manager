from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import psutil
import requests

# Configurar la dirección de tu servidor en la nube
server_address = "http://3.145.35.175:8080"

# Definir una función para enviar datos al servidor en la nube
def send_data_to_server(data, computer_id):
    url = f"{server_address}/data/{computer_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print(f"Datos enviados correctamente a {url}")
    else:
        print(f"Error al enviar datos a {url}: {response.status_code}, {response.text}")

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path_segments = self.path.split("/")
        if len(path_segments) >= 3 and path_segments[2] == "data":
            computer_id = path_segments[3]

            print(f"Solicitud recibida desde el computador {computer_id}")
            cpu_use = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage("/").percent

            # Crear un JSON con los datos
            data = {
                "CPUUsage": f"{cpu_use}%",
                "RAMUsage": f"{ram_usage}%",
                "DiskUsage": f"{disk_usage}%"
            }

            # Enviar los datos al servidor en nube
            send_data_to_server(data, computer_id)
        else:
            print(f"Solicitud desconocida recibida: {self.path}")
            # Manejar otras solicitudes según sea necesario
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
