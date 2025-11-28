from datetime import datetime, timedelta
from .modelos import Cliente, Vehiculo, Alquiler, Empleado, Estado, Mantenimiento, Incidente, TipoIncidente, Ambito, Categoria, TipoMantenimiento, CaracteristicaVehiculo
from BD.manager import CaracteristicaVehiculoManager, ClienteManager, VehiculoManager, AlquilerManager, EmpleadoManager, EstadoManager, MantenimientoManager, IncidenteManager, TipoIncidenteManager, AmbitoManager, CategoriaManager, TipoMantenimientoManager

class SistemaDeAlquiler:
    def __init__(self):
        # Inicializamos todos los Managers (la capa de Persistencia)
        self.cliente_manager = ClienteManager.ClienteManager()
        self.vehiculo_manager = VehiculoManager.VehiculoManager()
        self.alquiler_manager = AlquilerManager.AlquilerManager()
        self.empleado_manager = EmpleadoManager.EmpleadoManager()
        self.estado_manager = EstadoManager.EstadoManager()
        self.mantenimiento_manager = MantenimientoManager.MantenimientoManager()
        self.incidente_manager = IncidenteManager.IncidenteManager()
        self.tipo_incidente_manager = TipoIncidenteManager.TipoIncidenteManager()
        self.ambito_manager = AmbitoManager.AmbitoManager()
        self.categoria_manager = CategoriaManager.CategoriaManager()
        self.tipomantenimiento_manager = TipoMantenimientoManager.TipoMantenimientoManager()
        self.caracteristica_vehiculo_manager = CaracteristicaVehiculoManager.CaracteristicaVehiculoManager()

    ## ---------------------------------------------
    ## ABM DE CLIENTES Y EMPLEADOS (Ejemplo de delegación pura)
    ## ---------------------------------------------

    def crear_cliente(self, nombre, dni, telefono, mail):
        """Lógica de Alta: Crea el objeto y delega la persistencia."""
        cliente = Cliente.Cliente(nombre=nombre, dni=dni, telefono=telefono, mail=mail)
        # Aquí iría LÓGICA DE NEGOCIO (ej: validaciones complejas de DNI o reputación)
        return self.cliente_manager.guardar(cliente)
    
    def crear_empleado(self, nombre, dni, mail):
        """Lógica de Alta: Crea el objeto y delega la persistencia."""
        empleado = Empleado.Empleado(id_empleado=None, nombre=nombre, dni=dni, mail=mail)
        # Aquí iría LÓGICA DE NEGOCIO (ej: validaciones complejas de DNI o reputación)
        return self.empleado_manager.guardar(empleado)

    def obtener_cliente(self, id_cliente):
        return self.cliente_manager.obtener_por_id(id_cliente)
    
    def obtener_empleado(self, id_empleado):
        return self.empleado_manager.obtener_por_id(id_empleado)

    def listar_clientes(self):
        return self.cliente_manager.listar_todos()
    
    def listar_empleados(self):
        return self.empleado_manager.listar_todos()

    def modificar_cliente(self, id_cliente, data):
        """Lógica de Modificación: Obtener, modificar, delegar actualización."""
        cliente = self.obtener_cliente(id_cliente)
        if not cliente:
            return None
        
        # Lógica de Negocio: Aplicar los cambios
        cliente.nombre = data.get('nombre', cliente.nombre)
        cliente.dni = data.get('dni', cliente.dni)
        cliente.telefono = data.get('telefono', cliente.telefono)
        cliente.mail = data.get('mail', cliente.mail)
        
        return self.cliente_manager.actualizar(cliente)
    
    def modificar_empleado(self, id_empleado, data):
        """Lógica de Modificación: Obtener, modificar, delegar actualización."""
        empleado = self.obtener_empleado(id_empleado)
        if not empleado:
            return None
        
        # Lógica de Negocio: Aplicar los cambios
        empleado.nombre = data.get('nombre', empleado.nombre)
        empleado.dni = data.get('dni', empleado.dni)
        empleado.mail = data.get('mail', empleado.mail)
        
        return self.empleado_manager.actualizar(empleado)
    
    def eliminar_empleado(self, id_empleado):
        """Lógica de Baja: Delega la eliminación al manager."""
        # Aquí podrías agregar validaciones extra antes de eliminar
        return self.empleado_manager.eliminar(id_empleado)


    ## ---------------------------------------------
    ## GESTIÓN DE ALQUILERES (Lógica de Negocio Central)
    ## ---------------------------------------------
    
    def validar_disponibilidad_vehiculo(self, id_vehiculo, fecha_inicio, fecha_fin):
        """
        LÓGICA DE NEGOCIO: Verifica si un vehículo está disponible.
        (Esta lógica se movió del Manager a la capa de Servicio).
        """
        vehiculo = self.vehiculo_manager.obtener_por_id(id_vehiculo)
        

        if not vehiculo:
            return False
        
        
        
        if vehiculo.estado.id_estado in [3]: 
            print(f"❌Vehículo {id_vehiculo} en estado no operativo: {vehiculo.estado.estado}")
            return False

        
        esta_disponible = self.alquiler_manager.verificar_disponibilidad_sp(id_vehiculo, fecha_inicio, fecha_fin)

        if not esta_disponible:
            print(f"❌El vehículo {id_vehiculo} ya tiene reservas en esas fechas (Validado por SP).")
            return False

        return True
        
    def registrar_alquiler(self, id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin):
        """Aplica lógica de negocio para crear y persistir un alquiler."""
        
        ahora = datetime.now()
        
        if fecha_inicio < (ahora - timedelta(minutes=1)):
            print(f"❌Error: La fecha de inicio {fecha_inicio} es anterior a la actual.")
            return None

        # 2. Validar que la fecha fin no sea anterior a la de inicio
        if fecha_fin <= fecha_inicio:
            print(f"❌Error: La fecha de fin {fecha_fin} es anterior o igual a la de inicio.")
            return None


        # 1. Obtener objetos dependientes
        vehiculo = self.vehiculo_manager.obtener_por_id(id_vehiculo)
        cliente = self.cliente_manager.obtener_por_id(id_cliente)
        empleado = self.empleado_manager.obtener_por_id(id_empleado)
        
        if not (vehiculo and cliente and empleado):
            print("❌ Error: Faltan datos (Vehículo, Cliente o Empleado no encontrados).")
            return None
        
        # 2. LÓGICA CENTRAL: Validar disponibilidad
        if not self.validar_disponibilidad_vehiculo(id_vehiculo, fecha_inicio, fecha_fin):
            return None
        
        # 3. Calcular Costo y Crear objeto Alquiler
        estado_activo = self.estado_manager.obtener_por_id(6) # Estado 'Activo'
        
        nuevo_alquiler = Alquiler.Alquiler(
            id_alquiler=None, 
            vehiculo=vehiculo, 
            empleado=empleado, 
            cliente=cliente, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin, 
            costo_total=0, 
            estado=estado_activo
        )
        # El objeto Alquiler calcula su propio costo basado en la duración
        nuevo_alquiler.calcular_costo() 
        
        # 4. Persistir el alquiler y LÓGICA POST-PERSISTENCIA (Transacción)
        alquiler_persistido = self.alquiler_manager.guardar(nuevo_alquiler)
        
        if alquiler_persistido:
            return alquiler_persistido
            
        return None

    def modificar_alquiler(self, id_alquiler, data):
        """
        Modifica un alquiler. Permite actualizaciones parciales (ej: solo cambiar vehículo).
        """

        # 1. Buscamos el alquiler original
        alquiler = self.alquiler_manager.obtener_por_id(id_alquiler)
        if not alquiler:
            print(f"❌ Alquiler {id_alquiler} no encontrado.")
            return None

        recalcular_costo = False

        # 2. Actualización de Relaciones (Foreign Keys)
        # Solo buscamos el objeto en la BD si realmente vino el ID en 'data'
        
        if 'vehiculoId' in data:
            nuevo_vehiculo = self.vehiculo_manager.obtener_por_id(int(data['vehiculoId']))
            if nuevo_vehiculo:
                alquiler.vehiculo = nuevo_vehiculo
                recalcular_costo = True # Cambiar el auto puede cambiar el costo diario

        if 'clienteId' in data:
            nuevo_cliente = self.cliente_manager.obtener_por_id(int(data['clienteId']))
            if nuevo_cliente:
                alquiler.cliente = nuevo_cliente

        if 'empleadoId' in data:
            nuevo_empleado = self.empleado_manager.obtener_por_id(int(data['empleadoId']))
            if nuevo_empleado:
                alquiler.empleado = nuevo_empleado

        # 3. Actualización de Fechas
        if 'fechaInicio' in data and data['fechaInicio']:
            alquiler.fecha_inicio = data['fechaInicio'] 
            recalcular_costo = True

        if 'fechaFin' in data and data['fechaFin']:
            alquiler.fecha_fin = data['fechaFin']
            recalcular_costo = True

        if recalcular_costo:
            alquiler.calcular_costo()

        if not self.validar_disponibilidad_vehiculo(alquiler.vehiculo.id_vehiculo, alquiler.fecha_inicio, alquiler.fecha_fin):
            return None

        # 5. Guardar cambios
        exito = self.alquiler_manager.actualizar(alquiler)
        
        if exito:
            return alquiler
        return None
    

    def finalizar_alquiler(self, id_alquiler, km_final):
        """Proceso de finalización de un alquiler (Lógica de Negocio con transacción)."""
        alquiler = self.alquiler_manager.obtener_por_id(id_alquiler)
        
        if not alquiler and alquiler.estado.id_estado != 7:
            return False

        alquiler.finalizar_alquiler(km_final) 

        alquiler_actualizado = self.alquiler_manager.finalizar_con_kilometraje(alquiler)

        if alquiler_actualizado:
            return True
        return False
    
    # el eliminar pasa a ser cancelar, con el estado 5
    def cancelar_alquiler(self, id_alquiler):
        """Lógica de Cancelación de un Alquiler (si está en estado 'Activo')."""
        alquiler = self.alquiler_manager.obtener_por_id(id_alquiler)
        
        if not alquiler:
            print(f"❌ Alquiler {id_alquiler} no encontrado.")
            return False
        
        if alquiler.estado.id_estado not in [6, 7]: # 6 = Pendiente de inicio, 7 = En Curso
            print(f"❌ No se puede cancelar el alquiler {id_alquiler} porque no está activo.")
            return False
        
        # Delegar la cancelación al Manager
        exito = self.alquiler_manager.cancelar(alquiler)

        if exito:
            self.vehiculo_manager.actualizar_estado(alquiler.vehiculo.id_vehiculo, 1)
            return True
            
        return False
    


    ## ---------------------------------------------
    ## REPORTES
    ## ---------------------------------------------
    
    def generar_reporte_alquileres_por_cliente(self, id_cliente):
        # Esta consulta compleja debe ir en el AlquilerManager como un método específico.
        # return self.alquiler_manager.listar_por_cliente(id_cliente)
        pass # Implementación pendiente

    def listar_categorias(self):
        return self.categoria_manager.listar_todos()
    
    def listar_estados_por_ambito(self, ambito_id):
        return self.estado_manager.listar_por_ambito(ambito_id)
    
    def obtener_estado(self, id_estado):
        """Método auxiliar para obtener un objeto Estado completo."""
        return self.estado_manager.obtener_por_id(id_estado)

    # --- ABM DE VEHÍCULOS ---
    
    def crear_vehiculo(self, modelo, anio, id_categoria, patente, kilometraje, costo_diario, id_estado):
        """
        Lógica de Alta: Crea la característica, luego el vehículo.
        """
        
        # 1. Obtener objetos de consulta (dependencias)
        categoria = self.categoria_manager.obtener_por_id(id_categoria)
        # Usar el método auxiliar para obtener el objeto Estado
        estado_inicial = self.obtener_estado(id_estado)
        
        if not categoria or not estado_inicial:
            print(f"❌ Error: Categoría ({id_categoria}) o Estado ({id_estado}) inicial no encontrados.") 
            return None
        
        detalle = CaracteristicaVehiculoManager.CaracteristicaVehiculo(
            id_caracteristica=None,
            modelo=modelo,
            anio=anio,
            categoria=categoria
        )

        detalle = self.caracteristica_vehiculo_manager.guardar(detalle)
        
        if not detalle:
            return None

        # 3. Crear el objeto Vehiculo
        vehiculo = Vehiculo.Vehiculo(
            id_vehiculo=None,
            caracteristica_vehiculo=detalle,
            estado=estado_inicial,
            patente=patente,
            kilometraje=float(kilometraje), # Asegurar tipo numérico
            costo_diario=int(costo_diario) # Asegurar tipo entero
        )
        
        # 4. Persistir el objeto Vehículo
        return self.vehiculo_manager.guardar(vehiculo)
    
    def modificar_vehiculo(self, id_vehiculo, data):
        """Edita tanto la tabla VEHICULO como la tabla DETALLE_VEHICULO."""

        vehiculo = self.vehiculo_manager.obtener_por_id(id_vehiculo)
        if not vehiculo:
            print(f"❌ Vehículo {id_vehiculo} no encontrado.")
            return None

        # --- Actualizar DETALLE_VEHICULO ---
        detalle = vehiculo.caracteristica_vehiculo

        detalle.modelo = data.get("modelo", detalle.modelo)
        detalle.anio = data.get("anio", detalle.anio)

        if "categoriaId" in data:
            nueva_cat = self.categoria_manager.obtener_por_id(int(data["categoriaId"]))
            if not nueva_cat:
                print(f"❌ Categoría {data['categoriaId']} no encontrada.")
                return None
            detalle.categoria = nueva_cat

        ok_detalle = self.caracteristica_vehiculo_manager.actualizar(detalle)
        if not ok_detalle:
            print("❌ No se pudo actualizar DETALLE_VEHICULO.")
            return None

        # --- Actualizar VEHICULO ---
        vehiculo.patente = data.get("patente", vehiculo.patente)
        vehiculo.kilometraje = data.get("kilometraje", vehiculo.kilometraje)
        vehiculo.costo_diario = data.get("costoDiario", vehiculo.costo_diario)

        if "estadoId" in data:
            nuevo_estado = self.estado_manager.obtener_por_id(int(data["estadoId"]))
            if not nuevo_estado:
                print(f"❌ Estado {data['estadoId']} no encontrado.")
                return None
            vehiculo.estado = nuevo_estado

        ok_vehiculo = self.vehiculo_manager.actualizar(vehiculo)
        if not ok_vehiculo:
            print("❌ No se pudo actualizar VEHICULO.")
            return None

        return vehiculo

    def listar_vehiculos(self):
        """Retorna la lista de objetos Vehiculo completos."""
        # Delega al Manager que obtiene los datos e intenta resolver las FKs en el Manager.
        return self.vehiculo_manager.listar_todos()
    
    def eliminar_vehiculo(self, id_vehiculo):
        """Lógica de Eliminación de un Vehículo (si no tiene alquileres activos)."""
        vehiculo = self.vehiculo_manager.obtener_por_id(id_vehiculo)
        
        if not vehiculo:
            print(f"❌ Vehículo {id_vehiculo} no encontrado.")
            return False
        
        # LÓGICA DE NEGOCIO: Verificar que no tenga alquileres activos
        alquileres_activos = self.alquiler_manager.listar_activo_por_vehiculo(id_vehiculo)
        
        if len(alquileres_activos) > 0:
            print(f"❌ No se puede eliminar el vehículo {id_vehiculo} porque tiene alquileres activos.")
            return False
        
        return self.vehiculo_manager.eliminar(id_vehiculo)
    
    def verificar_estado_vehiculo_mantenimiento(self, id_vehiculo):
        """Verifica si el vehículo está en estado de mantenimiento (ID_ESTADO = 3)."""
        return self.vehiculo_manager.verificar_mantenimiento_activo(id_vehiculo) 

    # ----- ABM DE MANTENIMIENTOS -----

    def listar_tipo_mantenimientos(self):
        """Retorna la lista de tipos de mantenimiento."""
        return self.tipomantenimiento_manager.listar_todos()

    def registrar_mantenimiento(self, id_vehiculo, id_tipo_mantenimiento, tipo,fec_inicio, fec_fin, costo, observacion):
        """Lógica de Negocio para registrar un mantenimiento."""
        vehiculo = self.vehiculo_manager.obtener_por_id(id_vehiculo)
        tipo_mantenimiento = self.tipomantenimiento_manager.obtener_por_id(id_tipo_mantenimiento)

        if not vehiculo or not tipo_mantenimiento:
            print("❌ Vehículo o Tipo de Mantenimiento no encontrados.")
            return None
        
        mantenimiento = Mantenimiento.Mantenimiento(
            id_mantenimiento=None,
            vehiculo=vehiculo,
            tipo_mantenimiento=TipoMantenimiento.TipoMantenimiento(id_tipo_mantenimiento, tipo),
            fecha_inicio=fec_inicio,
            fecha_fin=fec_fin,
            costo=costo,
            observacion=observacion
        )

        mantenimiento = self.mantenimiento_manager.guardar(mantenimiento)

        if mantenimiento:
            if self.verificar_estado_vehiculo_mantenimiento(id_vehiculo):
                self.vehiculo_manager.actualizar_estado(id_vehiculo, 3) # 3 = 'Mantenimiento'
            else:
                self.vehiculo_manager.actualizar_estado(id_vehiculo, 1) # 1 = 'Disponible'
            return mantenimiento

        return None
    
    def finalizar_mantenimiento(self, id_mantenimiento):
        """Lógica de Negocio para finalizar un mantenimiento."""
        mantenimiento = self.mantenimiento_manager.obtener_por_id(id_mantenimiento)

        if not mantenimiento:
            print(f"❌ Mantenimiento {id_mantenimiento} no encontrado.")
            return False

        mantenimiento.fecha_fin = datetime.now()
        mantenimiento_actualizado = self.mantenimiento_manager.actualizar(mantenimiento)

        if mantenimiento_actualizado:
            self.vehiculo_manager.actualizar_estado(mantenimiento.vehiculo.id_vehiculo, 1)
            return True

        return False

    def eliminar_mantenimiento(self, id_mantenimiento, id_vehiculo):
        """Lógica de Negocio para eliminar un mantenimiento."""
        exito = self.mantenimiento_manager.eliminar_mantenimiento(id_mantenimiento)

        if exito:
            if self.verificar_estado_vehiculo_mantenimiento(id_vehiculo):
                self.vehiculo_manager.actualizar_estado(id_vehiculo, 3) # 3 = 'Mantenimiento'
            else:
                self.vehiculo_manager.actualizar_estado(id_vehiculo, 1) # 1 = 'Disponible'
            return True

        return False

    def listar_mantenimientos_por_vehiculo(self, id_vehiculo):
        """Retorna la lista de mantenimientos para un vehículo dado."""
        return self.mantenimiento_manager.listar_por_vehiculo(id_vehiculo)
    
    def modificar_mantenimiento(self, id_mantenimiento, data):
        """Lógica de Negocio para modificar un mantenimiento."""
        mantenimiento = self.mantenimiento_manager.obtener_por_id(id_mantenimiento)

        if not mantenimiento:
            print(f"❌ Mantenimiento {id_mantenimiento} no encontrado.")
            return None

        # Actualizar campos (Usando claves correctas y corchetes [])
        if "fec_inicio" in data:
            mantenimiento.fecha_inicio = data["fec_inicio"]
        if "fec_fin" in data:
            mantenimiento.fecha_fin = data["fec_fin"]
        if "descripcion" in data:
            mantenimiento.observacion = data["descripcion"]
        if "costo" in data:
            mantenimiento.costo = data["costo"]
            
        # Corrección de clave: 'id_tipo' (que es lo que manda routes)
        if "id_tipo" in data:
            tipo_mantenimiento = self.tipomantenimiento_manager.obtener_por_id(data["id_tipo"])
            if tipo_mantenimiento:
                mantenimiento.tipo_mantenimiento = tipo_mantenimiento

        mantenimiento_actualizado = self.mantenimiento_manager.actualizar(mantenimiento)

        if mantenimiento_actualizado:

            id_vehiculo = int(data['id_vehiculo'])
            

            if self.verificar_estado_vehiculo_mantenimiento(id_vehiculo):
                self.vehiculo_manager.actualizar_estado(id_vehiculo, 3) # 3 = 'Mantenimiento'
            else:
                self.vehiculo_manager.actualizar_estado(id_vehiculo, 1) # 1 = 'Disponible'
                
            return True

        return False

    #abm de incidentes
    def listar_tipos_incidentes(self):
        """Retorna la lista de tipos de incidentes."""
        return self.tipo_incidente_manager.listar_todos()
    
    def registrar_incidente(self, id_alquiler, id_tipo, fecha, descripcion):
        """Lógica para registrar un incidente asociado a un alquiler."""
        
        alquiler_obj = self.alquiler_manager.obtener_por_id(id_alquiler)
        
        tipo_obj = self.tipo_incidente_manager.obtener_por_id(id_tipo)

        if not alquiler_obj or not tipo_obj:
            print(f"❌ Error: Alquiler ({id_alquiler}) o Tipo Incidente ({id_tipo}) no encontrados.")
            return None

        # 3. Crear el objeto
        nuevo_incidente = Incidente.Incidente(
            id_incidente=None,
            tipo_incidente=tipo_obj,
            alquiler=alquiler_obj,
            fecha_incidente=fecha,
            descripcion=descripcion
        )

        # 4. Guardar
        return self.incidente_manager.guardar(nuevo_incidente)
    
    def listar_incidentes_por_alquiler(self, id_alquiler):
        """Retorna la lista de incidentes para un alquiler dado."""
        return self.incidente_manager.listar_por_alquiler(id_alquiler)
    
    
    def eliminar_incidente(self, id_incidente):
        """Lógica de Negocio para eliminar un incidente."""
        exito = self.incidente_manager.eliminar(id_incidente)

        if exito:
            return True

        return False