from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = {}  # Almacenamiento local para los datos de los computadores

@app.route('/data/<computer_id>', methods=['GET', 'POST'])
def receive_data(computer_id):
    try:
        if request.method == 'GET':
            # Devolver los datos de la computadora con el ID especificado
            data = data_store.get(computer_id)
            return jsonify(data), 200 if data else 404
        else:
            # Procesar los datos recibidos de la computadora
            data = request.json
            print(f"Datos recibidos de la computadora {computer_id}: {data}")  # Mensaje de depuración

            # Almacena los datos en el almacenamiento local
            data_store[computer_id] = data

            return f"Datos de la computadora {computer_id} recibidos y almacenados correctamente", 200
    except Exception as e:
        print(f"Error al procesar datos de la computadora {computer_id}: {e}")  # Mensaje de depuración
        return str(e), 400

@app.route('/')
def index():
    return '¡Bienvenido a mi servidor local en la nube!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
