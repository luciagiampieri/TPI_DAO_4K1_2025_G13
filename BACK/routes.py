from flask import Flask, app, request, jsonify 
from SistemaDeAlquiler import SistemaDeAlquiler

sistema = SistemaDeAlquiler()
app = Flask(__name__)

@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    """Endpoint para obtener la lista de clientes."""
    clientes = sistema.listar_clientes() # Llama a la capa de servicio
    
    clientes_data = [{
        'id': c.id_cliente, 
        'nombre': c.nombre, 
        'dni': c.dni, 
        'mail': c.mail
    } for c in clientes]
    
    return jsonify(clientes_data) # Devuelve la lista en formato JSON

@app.route('/api/clientes', methods=['POST'])
def alta_cliente():
    """Endpoint para dar de alta un nuevo cliente."""
    data = request.get_json()
    
    # Llama a la capa de servicio con la lógica de negocio (validación, etc.)
    cliente = sistema.crear_cliente(
        data['nombre'], data['dni'], data.get('telefono'), data.get('mail')
    )
    
    if cliente:
        return jsonify({
            "id": cliente.id_cliente, 
            "nombre": cliente.nombre
        }), 201 # 201 Created
    
    return jsonify({"error": "No se pudo crear el cliente."}), 400


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
