from flask import Flask, app, request, jsonify

from BACK.GestorReportes import GestorReportes 
from .SistemaDeAlquiler import SistemaDeAlquiler
from datetime import datetime

sistema = SistemaDeAlquiler()
gestor_reportes = GestorReportes()
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

@app.route('/api/clientes/<int:id_cliente>', methods=['DELETE'])
def eliminar_cliente(id_cliente):
    exito = sistema.cliente_manager.eliminar(id_cliente)

    if exito:
        return jsonify({"mensaje": "Cliente eliminado correctamente."}), 200
    
    return jsonify({"error": "No se pudo eliminar el cliente."}), 400

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

#obtener vehiculo por id
@app.route('/api/vehiculos/<int:id_vehiculo>', methods=['GET'])
def obtener_vehiculo_por_id(id_vehiculo):
    """Endpoint para obtener el detalle de un vehículo por su ID."""
    vehiculo = sistema.vehiculo_manager.obtener_por_id(id_vehiculo)
    
    if not vehiculo:
        return jsonify({"error": "Vehículo no encontrado."}), 404
    
    vehiculo_data = {
        'id': vehiculo.id_vehiculo,
        'patente': vehiculo.patente,
        'kilometraje': vehiculo.kilometraje,
        'costo_diario': vehiculo.costo_diario,
        'estado': vehiculo.estado.estado, # Obtenemos el nombre del estado
        'modelo': vehiculo.caracteristica_vehiculo.modelo, # Obtenemos el modelo
        'anio': vehiculo.caracteristica_vehiculo.anio,
        'categoria': vehiculo.caracteristica_vehiculo.categoria.categoria # Obtenemos la categoría
    }
    
    return jsonify(vehiculo_data)

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

# --- RUTAS DE EMPLEADOS (Para el Dropdown) ---
@app.route('/api/empleados', methods=['GET'])
def listar_empleados():
    empleados = sistema.empleado_manager.listar_todos()
    
    data = [{'id': e.id_empleado, 'nombre': e.nombre} for e in empleados]
    return jsonify(data)

# --- RUTAS DE ALQUILERES ---
@app.route('/api/alquileres', methods=['GET'])
def listar_alquileres():
    alquileres = sistema.alquiler_manager.listar_todos()
    
    # Serializamos con datos anidados para mostrar nombres en la tabla
    data = [{
        'id': a.id_alquiler,
        'vehiculo': a.vehiculo.patente + ' - ' + a.vehiculo.caracteristica_vehiculo.modelo,
        'cliente': a.cliente.nombre,
        'empleado': a.empleado.nombre,
        'fecha_inicio': a.fecha_inicio.strftime('%Y-%m-%d %H:%M'),
        'fecha_fin': a.fecha_fin.strftime('%Y-%m-%d %H:%M'),
        'costo_total': a.costo_total,
        'estado': a.estado.estado
    } for a in alquileres]
    
    return jsonify(data)

@app.route('/api/alquileres', methods=['POST'])
def crear_alquiler():
    data = request.get_json()
    
    try:
        # Convertir strings de fecha (del JSON) a objetos datetime
        f_inicio = datetime.strptime(data['fechaInicio'], '%Y-%m-%dT%H:%M')
        f_fin = datetime.strptime(data['fechaFin'], '%Y-%m-%dT%H:%M')
        
        # Llamar a la lógica del sistema (que valida disponibilidad)
        alquiler = sistema.registrar_alquiler(
            int(data['vehiculoId']),
            int(data['clienteId']),
            int(data['empleadoId']),
            f_inicio,
            f_fin
        )
        
        if alquiler:
            return jsonify({"mensaje": "Alquiler registrado con éxito"}), 201
        else:
            return jsonify({"error": "No se pudo registrar. El vehículo podría no estar disponible."}), 400
            
    except ValueError as e:
        return jsonify({"error": f"Error de formato de fecha: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#eliminar alquiler
@app.route('/api/alquileres/<int:id_alquiler>', methods=['DELETE'])
def eliminar_alquiler(id_alquiler):
    exito = sistema.eliminar_alquiler(id_alquiler)
    
    if exito:
        return jsonify({"mensaje": "Alquiler eliminado correctamente."}), 200
    else:
        return jsonify({"error": "No se pudo eliminar el alquiler."}), 400
    
#modificar alquiler
@app.route('/api/alquileres/<int:id_alquiler>', methods=['PUT'])
def modificar_alquiler(id_alquiler):
    data = request.get_json()
    
    try:
        f_inicio = datetime.strptime(data['fechaInicio'], '%Y-%m-%dT%H:%M')
        f_fin = datetime.strptime(data['fechaFin'], '%Y-%m-%dT%H:%M')
        
        alquiler_modificado = sistema.modificar_alquiler(
            id_alquiler,
            int(data['vehiculoId']),
            int(data['clienteId']),
            int(data['empleadoId']),
            f_inicio,
            f_fin
        )
        
        if alquiler_modificado:
            return jsonify({"mensaje": "Alquiler modificado con éxito"}), 200
        else:
            return jsonify({"error": "No se pudo modificar el alquiler."}), 400
            
    except ValueError as e:
        return jsonify({"error": f"Error de formato de fecha: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#finalizar alquiler
@app.route('/api/alquileres/finalizar/<int:id_alquiler>', methods=['POST'])
def finalizar_alquiler(id_alquiler):
    data = request.get_json()
    
    try:
        km_final = float(data['kilometrajeFinal'])
        
        exito = sistema.finalizar_alquiler(id_alquiler, km_final)
        
        if exito:
            return jsonify({"mensaje": "Alquiler finalizado con éxito"}), 200
        else:
            return jsonify({"error": "No se pudo finalizar el alquiler."}), 400
            
    except ValueError as e:
        return jsonify({"error": f"Error de formato de kilometraje: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#-------------------------------
#--- RUTAS DE MANTENIMIENTOS ---
#-------------------------------
@app.route('/api/mantenimientos/vehiculo/<int:id_vehiculo>', methods=['GET'])
def listar_mantenimientos_vehiculo(id_vehiculo):
    mantenimientos = sistema.listar_mantenimientos_por_vehiculo(id_vehiculo)
    
    data = [{
        'id': m.id_mantenimiento,
        'vehiculo': m.vehiculo.patente + ' - ' + m.vehiculo.caracteristica_vehiculo.modelo,
        'tipo_mantenimiento': m.tipo_mantenimiento.tipo_mantenimiento,
        'fecha_inicio': m.fecha_inicio.strftime('%Y-%m-%d %H:%M'),
        'fecha_fin': m.fecha_fin.strftime('%Y-%m-%d %H:%M') if m.fecha_fin else None,
        'costo': m.costo,
        'descripcion': m.observacion
    } for m in mantenimientos]
    
    return jsonify(data)

#liminar un mantenimiento
@app.route('/api/mantenimientos/<int:id_mantenimiento>', methods=['DELETE'])
def eliminar_mantenimiento(id_mantenimiento):
    exito = sistema.eliminar_mantenimiento(id_mantenimiento)
    
    if exito:
        return jsonify({"mensaje": "Mantenimiento eliminado correctamente."}), 200
    else:
        return jsonify({"error": "No se pudo eliminar el mantenimiento."}), 400

#crear un mantenimiento
@app.route('/api/mantenimientos', methods=['POST'])
def crear_mantenimiento():
    data = request.get_json()
    
    try:
        f_inicio = datetime.strptime(data['fechaInicio'], '%Y-%m-%dT%H:%M')
        f_fin = (
            datetime.strptime(data['fechaFin'], '%Y-%m-%dT%H:%M') 
            if data.get('fechaFin') else None
        )
        
        mantenimiento = sistema.registrar_mantenimiento(
            int(data['vehiculoId']),
            int(data['tipo_mantenimiento_id']),
            f_inicio,
            f_fin,
            float(data['costo']),
            data.get('descripcion', '')
        )
        
        if mantenimiento:
            return jsonify({"mensaje": "Mantenimiento registrado con éxito"}), 201
        else:
            return jsonify({"error": "No se pudo registrar el mantenimiento."}), 400
            
    except ValueError as e:
        return jsonify({"error": f"Error de formato de fecha o costo: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/tipos_mantenimiento', methods=['GET'])
def listar_tipos_mantenimiento():
    tipos = sistema.listar_tipo_mantenimientos()
    
    data = [{
        'id': t.id_tipo_mantenimiento,
        'tipo_mantenimiento': t.tipo_mantenimiento
    } for t in tipos]
    
    return jsonify(data)


# --- RUTAS DE REPORTES  ---

@app.route('/api/reportes/ranking', methods=['GET'])
def reporte_ranking():
    data = gestor_reportes.obtener_ranking_vehiculos()
    return jsonify(data)

@app.route('/api/reportes/facturacion/<int:anio>', methods=['GET'])
def reporte_facturacion(anio):
    data = gestor_reportes.obtener_facturacion_anual(anio)
    return jsonify(data)

@app.route('/api/reportes/cliente/<int:id_cliente>', methods=['GET'])
def reporte_cliente(id_cliente):
    data = gestor_reportes.obtener_historial_cliente(id_cliente)
    for d in data:
        if d['FEC_INICIO']: d['FEC_INICIO'] = d['FEC_INICIO'].strftime('%Y-%m-%d')
        if d['FEC_FIN']: d['FEC_FIN'] = d['FEC_FIN'].strftime('%Y-%m-%d')
    return jsonify(data)

@app.route('/api/reportes/periodo', methods=['POST'])
def reporte_periodo():
    """Reporte de alquileres filtrados por rango de fechas."""
    body = request.get_json()
    
    if not body or 'desde' not in body or 'hasta' not in body:
        return jsonify({"error": "Faltan parámetros 'desde' y 'hasta'"}), 400

    data = gestor_reportes.obtener_reporte_periodo(body['desde'], body['hasta'])
    
    for d in data: 
        if d.get('FEC_INICIO'): 
            d['FEC_INICIO'] = d['FEC_INICIO'].strftime('%Y-%m-%d %H:%M')
        if d.get('FEC_FIN'): 
            d['FEC_FIN'] = d['FEC_FIN'].strftime('%Y-%m-%d %H:%M')
        
    return jsonify(data)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
