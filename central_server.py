import socket
import json
import threading

server_ip = "0.0.0.0"
server_port = 8000
client_connections = []

# Contador para asignar IDs únicos
client_id_counter = 1

def handle_client(client_socket):
    global client_id_counter

    # Asignar un ID único al cliente remoto
    client_id = client_id_counter
    client_id_counter += 1

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            received_data = json.loads(data.decode())

            # Agregar el ID al mensaje
            received_data["ID"] = client_id

            # Procesar los datos
            print("Received data:", received_data)

    except Exception as e:
        print(f"Error handling client connection: {e}")
    finally:
        client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)

    print(f"Server started on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        client_connections.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    run_server()
