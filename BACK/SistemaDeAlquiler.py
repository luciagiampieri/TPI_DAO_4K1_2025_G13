# SistemaDeAlquiler.py

from datetime import datetime
# Importamos todas las clases de dominio que vamos a usar
from .modelos import Cliente, Vehiculo, Alquiler, Empleado, Estado
# Importamos todos los Managers necesarios para la orquestación
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
    ## ABM DE CLIENTES (Ejemplo de delegación pura)
    ## ---------------------------------------------

    def crear_cliente(self, nombre, dni, telefono, mail):
        """Lógica de Alta: Crea el objeto y delega la persistencia."""
        cliente = Cliente.Cliente(nombre=nombre, dni=dni, telefono=telefono, mail=mail)
        # Aquí iría LÓGICA DE NEGOCIO (ej: validaciones complejas de DNI o reputación)
        return self.cliente_manager.guardar(cliente)

    def obtener_cliente(self, id_cliente):
        return self.cliente_manager.obtener_por_id(id_cliente)

    def listar_clientes(self):
        return self.cliente_manager.listar_todos()

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


    ## ---------------------------------------------
    ## GESTIÓN DE ALQUILERES (Lógica de Negocio Central)
    ## ---------------------------------------------
    
    def __validar_disponibilidad_vehiculo(self, id_vehiculo, fecha_inicio, fecha_fin):
        """
        LÓGICA DE NEGOCIO: Verifica si un vehículo está disponible.
        (Esta lógica se movió del Manager a la capa de Servicio).
        """
        vehiculo = self.vehiculo_manager.obtener_por_id(id_vehiculo)
        
        # Asumimos ID 101 es 'Disponible' para Vehículos
        if not vehiculo or vehiculo.estado.id_estado != 101:
            print(f"❌ Vehículo {id_vehiculo} no disponible por estado actual ({vehiculo.estado.estado}).")
            return False

        # Verifica solapamiento de fechas en alquileres ACTIVO (ID_ESTADO = 201)
        # Esto debe ser implementado con una consulta específica en el AlquilerManager
        # o directamente aquí si se considera lógica simple de consulta.
        
        # Una implementación simplificada de la consulta (que debería ir en el Manager):
        alquileres_solapados = self.alquiler_manager.buscar_alquileres_solapados(
            id_vehiculo, fecha_inicio, fecha_fin, estado_alquiler_id=201
        )
        
        if alquileres_solapados:
            print(f"❌ Vehículo {id_vehiculo} tiene alquileres activos que se solapan.")
            return False
        
        # También se debería chequear mantenimiento
        # MantenimientoManager.buscar_mantenimientos_solapados(...)
            
        return True # Disponible
        
    def registrar_alquiler(self, id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin):
        """Aplica lógica de negocio para crear y persistir un alquiler."""
        
        # 1. Obtener objetos dependientes
        vehiculo = self.vehiculo_manager.obtener_por_id(id_vehiculo)
        cliente = self.cliente_manager.obtener_por_id(id_cliente)
        empleado = self.empleado_manager.obtener_por_id(id_empleado)
        
        if not (vehiculo and cliente and empleado):
            print("❌ Error: Faltan datos (Vehículo, Cliente o Empleado no encontrados).")
            return None
        
        # 2. LÓGICA CENTRAL: Validar disponibilidad
        if not self.__validar_disponibilidad_vehiculo(id_vehiculo, fecha_inicio, fecha_fin):
            return None
        
        # 3. Calcular Costo y Crear objeto Alquiler
        estado_activo = self.estado_manager.obtener_por_id(201) # Estado 'Activo'
        
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
            # LÓGICA DE NEGOCIO: Cambiar estado del vehículo DESPUÉS de persistir el alquiler
            self.vehiculo_manager.actualizar_estado(id_vehiculo, 102) # 102 = 'Alquilado'
            return alquiler_persistido
            
        return None
        
    def finalizar_alquiler(self, id_alquiler, km_final):
        """Proceso de finalización de un alquiler (Lógica de Negocio con transacción)."""
        alquiler = self.alquiler_manager.obtener_por_id(id_alquiler)
        
        if not alquiler or alquiler.estado.id_estado != 201: # 201 = Activo
            return False

        alquiler.finalizar_alquiler(km_final) 
        alquiler_actualizado = self.alquiler_manager.actualizar(alquiler)

        if alquiler_actualizado:
            self.vehiculo_manager.actualizar_estado(alquiler.vehiculo.id_vehiculo, 101) 
            return True
        return False
    
    def eliminar_alquiler(self, id_alquiler):
        """Lógica de Eliminación de un Alquiler (si está en estado 'Activo')."""
        alquiler = self.alquiler_manager.obtener_por_id(id_alquiler)
        
        if not alquiler:
            print(f"❌ Alquiler {id_alquiler} no encontrado.")
            return False
        
        if alquiler.estado.id_estado != 201: # 201 = Activo
            print(f"❌ No se puede eliminar el alquiler {id_alquiler} porque no está activo.")
            return False
        
        # Delegar la eliminación al Manager
        return self.alquiler_manager.eliminar(id_alquiler)


    ## ---------------------------------------------
    ## REPORTES
    ## ---------------------------------------------

    # Los métodos de reportes irían aquí, usando métodos de consulta en los Managers.
    # Ej: reporte_alquileres_por_cliente, reporte_vehiculos_mas_alquilados, etc.
    
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

        # 2. Crear y persistir la Característica/Detalle del Vehículo
        # NOTA: Debes pasar el objeto Categoria, no solo el ID, si el Manager lo espera.
        detalle = self.caracteristica_vehiculo_manager.crear_detalle(modelo, anio, categoria)
        
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
        alquileres_activos = self.alquiler_manager.listar_por_vehiculo(id_vehiculo)
        
        if len(alquileres_activos) > 0:
            print(f"❌ No se puede eliminar el vehículo {id_vehiculo} porque tiene alquileres activos.")
            return False
        
        return self.vehiculo_manager.eliminar(id_vehiculo)
    

