import requests
import json

def main():
    # Realiza una petición GET a la ruta /data/1
    response = requests.get("http://3.14.135.44:8080/data/1")

    # Si la petición fue exitosa, muestra el tipo de objeto JSON
    if response.status_code == 200:
        # Decodifica el objeto JSON
        data = response.content.decode()

        # Deserializa el objeto JSON en un objeto Python
        data = json.loads(data)

        # Imprime el tipo de objeto JSON
        print(type(data))

    else:
        # Imprime un mensaje de error
        print("Error al realizar la petición")

if __name__ == "__main__":
    main()
