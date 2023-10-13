from flask import Flask, request, jsonify

app = Flask(__name__)

# Datos recopilados del servidor central
own_data = {
    "ID": "ServerCentral",
    "CPUUsage": 0.0,
    "RAMUsage": 0.0,
    "DiskUsage": 0.0
}

# Ruta para recibir datos del cliente remoto
@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()
    print("Received data from client:", data)

    # Realiza cualquier procesamiento adicional si es necesario
    # ...

    return "Data received successfully", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
