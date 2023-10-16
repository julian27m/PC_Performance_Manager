from flask import Flask, request, jsonify
import boto3
import json
import os

app = Flask(__name__)

# Utiliza os.environ para acceder a las variables de entorno
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Estructura de datos para almacenar información dinámica
dynamic_data = {}

# Configura el acceso a AWS S3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

@app.route('/data/<computer_id>', methods=['GET', 'POST'])
def receive_data(computer_id):
    if request.method == 'GET':
        # Aquí debes obtener los datos dinámicos de la computadora con ID específico
        if computer_id in dynamic_data:
            data = dynamic_data[computer_id]
            return jsonify(data)
        else:
            return 'No se encontraron datos para la computadora', 404

    if request.method == 'POST':
        try:
            data = request.json

            file_name = f'{computer_id}.json'
            s3.put_object(Bucket='nombre-del-bucket', Key=file_name, Body=json.dumps(data))

            # Almacena la información dinámica para la computadora
            dynamic_data[computer_id] = data

            return f"Datos de la computadora {computer_id} recibidos y almacenados correctamente", 200
        except Exception as e:
            return str(e), 400

@app.route('/')
def index():
    return '¡Bienvenido a mi servidor en la nube!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
