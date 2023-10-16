import requests
import json
import psutil
import time

# Dirección del servidor
server_url = "http://3.14.135.44:8080/data/1"

while True:
    # Obtener las estadísticas del computador remoto
    cpu_use = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent

    # Crear un diccionario con los datos
    data = {
        "CPUUsage": f"{cpu_use}%",
        "RAMUsage": f"{ram_usage}%",
        "DiskUsage": f"{disk_usage}%"
    }

    headers = {"Content-Type": "application/json"}

    # Enviar los datos al servidor
    response = requests.post(server_url, data=json.dumps(data, indent=None), headers=headers)

    if response.status_code == 200:
        try:
            responseData = response.content.decode()
            print(responseData)
        except Exception as e:
            print(e)
    else:
        print("Error al enviar los datos.")

    # Esperar 5 segundos antes de enviar nuevamente
    time.sleep(5)
