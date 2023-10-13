import socket
import json
import psutil
import time

# Dirección del servidor central
server_address = "157.253.192.187"  
server_port = 8000

# Función para enviar datos al servidor central
def send_data_to_server(data, client_id, server_socket):
    data["ID"] = client_id
    data_json = json.dumps(data)
    server_socket.send(data_json.encode())

# Función para obtener el ID único del cliente remoto (si es necesario)
def assign_client_id(server_socket):
    # Implementa esta función si deseas asignar un ID al cliente desde el servidor central
    pass

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    client_id = assign_client_id(client_socket)

    while True:
        # Recopila los datos en este loop
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent

        data = {
            "CPUUsage": cpu_usage,
            "RAMUsage": ram_usage,
            "DiskUsage": disk_usage
        }

        # Envía los datos al servidor central
        send_data_to_server(data, client_id, client_socket)

        time.sleep(5)  # Ajusta la frecuencia de envío según sea necesario
