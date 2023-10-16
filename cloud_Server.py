from flask import Flask, request, jsonify
import boto3
import json
import os

app = Flask(__name__)

# Utiliza os.environ para acceder a las variables de entorno
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Configura el acceso a AWS S3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


@app.route('/data/<computer_id>', methods=['POST'])
def receive_data(computer_id):
    try:
        data = request.json

        file_name = f'{computer_id}.json'
        s3.put_object(Bucket='nombre-del-bucket', Key=file_name, Body=json.dumps(data))

        return f"Datos de la computadora {computer_id} recibidos y almacenados correctamente", 200
    except Exception as e:
        return str(e), 400
    
@app.route('/')
def index():
    return '¡Bienvenido a mi servidor en la nube!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
