from flask import Flask, app, request, jsonify 
from .SistemaDeAlquiler import SistemaDeAlquiler

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


@app.route('/api/clientes/<int:id_cliente>', methods=['PUT'])
def actualizar_cliente(id_cliente):
    data = request.get_json()

    cliente_mod = sistema.modificar_cliente(id_cliente, data)

    if cliente_mod:
        return jsonify({
            "id": id_cliente,
            "nombre": data.get("nombre"),
            "dni": data.get("dni"),
            "telefono": data.get("telefono"),
            "mail": data.get("mail")
        }), 200

    return jsonify({"error": "No se pudo actualizar el cliente."}), 400


@app.route('/api/categoria', methods=['GET'])
def listar_categorias():
    """Endpoint para obtener las categorías de vehículos (tabla lookup)."""
    # Suponiendo que tienes un Manager llamado CategoriaManager
    categorias = sistema.listar_categorias() 
    
    categorias_data = [{
        'id': c.id_categoria, 
        'nombre': c.categoria 
    } for c in categorias]
    
    return jsonify(categorias_data)


@app.route('/api/estados/<int:ambito_id>', methods=['GET'])
def listar_estados_por_ambito(ambito_id):
    """Endpoint para obtener los estados válidos para Vehiculos (Ámbito 1)."""
    # El ID de Ámbito para Vehículos es 1 (según tu script SQL)
    estados = sistema.listar_estados_por_ambito(ambito_id=ambito_id) 
    
    estados_data = [{
        'id': e.id_estado, 
        'nombre': e.estado
    } for e in estados]
    
    return jsonify(estados_data)

@app.route('/api/vehiculos', methods=['GET'])
def detalle_vehiculo():
    """Endpoint para obtener el detalle de un vehículo por su ID."""
    vehiculos = sistema.listar_vehiculos()
    
    if not vehiculos:
        return jsonify({"error": "Vehículo no encontrado."}), 404
    
    vehiculos_data = [{
        'id': v.id_vehiculo,
        'patente': v.patente,
        'kilometraje': v.kilometraje,
        'costo_diario': v.costo_diario,
        'estado': v.estado.estado, # Obtenemos el nombre del estado
        'modelo': v.caracteristica_vehiculo.modelo, # Obtenemos el modelo
        'anio': v.caracteristica_vehiculo.anio,
        'categoria': v.caracteristica_vehiculo.categoria.categoria # Obtenemos la categoría
    } for v in vehiculos]
    
    return jsonify(vehiculos_data)

@app.route('/api/vehiculos', methods=['POST'])
def alta_vehiculo():
    """Endpoint para dar de alta un nuevo vehículo."""
    data = request.get_json()
    
    # Llama a la capa de servicio con la lógica de negocio y persistencia
    vehiculo = sistema.crear_vehiculo(
        modelo=data['modelo'],
        anio=data['anio'],
        id_categoria=int(data['categoriaId']), # Convertir a INT
        patente=data['patente'],
        kilometraje=float(data.get('kilometraje', 0)), # Usar valor por defecto
        costo_diario=data['costoDiario'],
        id_estado=int(data['estadoId']) # Estado inicial (ej: Disponible)
    )
    
    if vehiculo:
        return jsonify({
            "id": vehiculo.id_vehiculo, 
            "patente": vehiculo.patente,
            "modelo": vehiculo.caracteristica_vehiculo.modelo
        }), 201 # 201 Created
    
    return jsonify({"error": "No se pudo crear el vehículo. Revise DNI o datos faltantes."}), 400

# eliminar vehiculo
@app.route('/api/vehiculos/<int:id_vehiculo>', methods=['DELETE'])
def eliminar_vehiculo(id_vehiculo):
    """Endpoint para eliminar un vehículo por su ID y detalle."""
    exito = sistema.eliminar_vehiculo(id_vehiculo)
    
    if exito:
        return jsonify({"mensaje": "Vehículo eliminado correctamente."}), 200
    else:
        return jsonify({"error": "No se pudo eliminar el vehículo."}), 400
    

@app.route('/api/vehiculos/<int:id_vehiculo>', methods=['PUT'])
def actualizar_vehiculo(id_vehiculo):
    data = request.get_json()

    veh_mod = sistema.modificar_vehiculo(id_vehiculo, data)

    if veh_mod:
        return jsonify({
            "id": veh_mod.id_vehiculo,
            "patente": veh_mod.patente,
            "kilometraje": veh_mod.kilometraje,
            "costo_diario": veh_mod.costo_diario,
            "estado": veh_mod.estado.estado,
            "modelo": veh_mod.caracteristica_vehiculo.modelo,
            "anio": veh_mod.caracteristica_vehiculo.anio,
            "categoria": veh_mod.caracteristica_vehiculo.categoria.categoria
        }), 200

    return jsonify({"error": "No se pudo actualizar el vehículo."}), 400



if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
