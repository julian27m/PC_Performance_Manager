import json
import psutil
import requests

# Dirección del servidor central
server_address = "http://157.253.192.187:8000"

# En este ejemplo, el servidor central se identifica con ID 0
server_id = 0

# Asignación de ID: el servidor central asigna IDs únicos a los clientes remotos
def assign_client_id():
    response = requests.get(f"{server_address}/assign_id")
    if response.status_code == 200:
        return response.json()["client_id"]
    else:
        print("Failed to assign client ID.")
        return None

# Envío de datos al servidor central
def send_data_to_server(data, client_id):
    url = f"{server_address}/data"
    headers = {'Content-Type': 'application/json'}

    data["ID"] = client_id

    # Enviar datos como JSON al servidor central
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        print("Data sent successfully")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")

# Recopilación y envío de datos
def collect_data(client_id):
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent

    data = {
        "CPUUsage": cpu_usage,
        "RAMUsage": ram_usage,
        "DiskUsage": disk_usage
    }

    send_data_to_server(data, client_id)

if __name__ == "__main__":
    # Asignar un ID único al cliente remoto
    client_id = assign_client_id()

    if client_id is not None:
        # Iniciar la recopilación y el envío de datos
        while True:
            collect_data(client_id)
