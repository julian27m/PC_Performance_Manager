from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import psutil

# Configurar la dirección de tu servidor en la nube
server_address = "http://3.14.135.44:8080"

def check_server_connectivity():
    try:
        response = requests.get(server_address)
        response.raise_for_status()
        print("Conexión exitosa con el servidor en nube.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error al conectarse al servidor en nube: {str(e)}")
        return False

# Definir una función para enviar datos al servidor en nube
def send_data_to_server(data, computer_id):
    url = f"{server_address}/data/{computer_id}"
    headers = {"Content-Type": "application/json"}

    # Intentar enviar datos al servidor en nube
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Esto lanzará una excepción si hay un error HTTP

        print(f"Datos enviados correctamente a {url}")
    except Exception as e:
        print(f"Error al enviar datos a {url}: {str(e)}")

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path_segments = self.path.split("/")
        if len(path_segments) >= 3 and path_segments[2] == "data":
            computer_id = path_segments[3]
            print(f"ID del computador: {computer_id}")  # Mensaje de depuración

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

            print(f"JSON enviado a servidor en nube: {json.dumps(data)}")  # Mensaje de depuración
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
    if check_server_connectivity():
        run()
    else:
        print("No se pudo establecer conexión con el servidor en nube. Revise la conectividad antes de iniciar el servidor local.")
