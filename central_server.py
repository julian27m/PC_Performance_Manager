import socket
import json
import threading

# Dirección y puerto del servidor central
server_ip = "0.0.0.0"  # Escucha en todas las interfaces
server_port = 8000

# Lista para almacenar las conexiones de los clientes remotos
client_connections = []

# Función para manejar las conexiones de los clientes remotos
def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # Decodificar los datos recibidos (asumimos que son JSON)
            received_data = json.loads(data.decode())

            # Aquí puedes procesar los datos según tus necesidades
            print("Received data:", received_data)

    except Exception as e:
        print(f"Error handling client connection: {e}")
    finally:
        client_socket.close()

# Función principal del servidor
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
