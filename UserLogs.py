import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/obtener-logs', methods=['GET'])
def obtener_logs():
    url = "https://10.111.101.253/api/v2/log/memory/event/user?start=0&rows=500&filter=subtype==user"
    
    # Extraer el token de autorización del encabezado de la solicitud
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token de autorización no proporcionado"}), 400

    headers = {"Authorization": token}
    response = requests.get(url, headers=headers, verify=False)  # Desactivar la verificación del certificado

    
    if response.status_code == 200:
         results = response.json().get('results', [])
         userLogs = [ 
             { "accion": result['action'], 
              "Fecha": result['date'], 
              "Mensaje": result['msg'], 
              "Hora": result['time'],
              "Usuario": result['user'] 
            } for result in results ]
         return jsonify({"UserLogs": userLogs})
    else: 
        return jsonify({"error": "Failed to fetch user logs"}), 500

if __name__ == '__main__':
    app.run(debug=True)
