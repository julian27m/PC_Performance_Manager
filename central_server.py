import socket
import json
import psutil
import threading
import time

# Variables para los datos del servidor central
own_cpu_usage = 0.0
own_ram_usage = 0.0
own_disk_usage = 0.0

# Variable para asignar IDs a los clientes remotos
next_client_id = 0

# Configuración para el servidor
SERVER_IP = "157.253.192.187"  # Escucha en todas las interfaces
SERVER_PORT = 8000  # Puerto para la comunicación con los clientes
BUFFER_SIZE = 1024

# Función para enviar datos a un cliente
def send_data_to_client(client_socket, data):
    try:
        data_json = json.dumps(data)
        client_socket.send(data_json.encode())
    except Exception as e:
        print(f"Error sending data to client: {e}")

# Función para asignar un ID único a un cliente remoto
def assign_client_id():
    global next_client_id
    next_client_id += 1
    return next_client_id

# Función para manejar la conexión con un cliente
def handle_client(client_socket):
    global own_cpu_usage, own_ram_usage, own_disk_usage

    while True:
        try:
            # Recopila los datos propios del servidor
            own_cpu_usage = psutil.cpu_percent(interval=1)
            own_ram_usage = psutil.virtual_memory().percent
            own_disk_usage = psutil.disk_usage("/").percent
            own_data = {
                "ID": "ServerCentral",
                "CPUUsage": own_cpu_usage,
                "RAMUsage": own_ram_usage,
                "DiskUsage": own_disk_usage
            }

            # Envía los datos al cliente
            send_data_to_client(client_socket, own_data)

            # Espera un intervalo de tiempo antes de enviar nuevamente
            time.sleep(5)
        except Exception as e:
            print(f"Error handling client connection: {e}")
            break

# Función principal del servidor
def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)

    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
