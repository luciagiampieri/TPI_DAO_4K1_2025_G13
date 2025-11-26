# SistemaDeAlquiler.py

from datetime import datetime
# Importamos todas las clases de dominio que vamos a usar
from BACK.modelos import Cliente, Vehiculo, Alquiler, Empleado, Estado
# Importamos todos los Managers necesarios para la orquestación
from ..BD.manager import CaracteristicaVehiculoManager, ClienteManager, VehiculoManager, AlquilerManager, EmpleadoManager, EstadoManager, MantenimientoManager, IncidenteManager, TipoIncidenteManager, AmbitoManager, CategoriaManager, TipoMantenimientoManager

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

        # 1. LÓGICA DE NEGOCIO: El objeto Alquiler realiza la lógica de finalización
        alquiler.finalizar_alquiler(km_final) 
        
        # 2. Persistencia de la modificación del Alquiler (ID_ESTADO=202, COSTO_TOTAL, FEC_FIN)
        alquiler_actualizado = self.alquiler_manager.actualizar(alquiler)
        
        if alquiler_actualizado:
            # 3. LÓGICA DE NEGOCIO: Liberar vehículo (ID_ESTADO=101)
            self.vehiculo_manager.actualizar_estado(alquiler.vehiculo.id_vehiculo, 101) 
            # 4. Persistencia: Actualizar kilometraje del vehículo (requiere método en VehiculoManager)
            # self.vehiculo_manager.actualizar_kilometraje(alquiler.vehiculo.id_vehiculo, km_final)
            return True
            
        return False

    ## ---------------------------------------------
    ## REPORTES
    ## ---------------------------------------------

    # Los métodos de reportes irían aquí, usando métodos de consulta en los Managers.
    # Ej: reporte_alquileres_por_cliente, reporte_vehiculos_mas_alquilados, etc.
    
    def generar_reporte_alquileres_por_cliente(self, id_cliente):
        # Esta consulta compleja debe ir en el AlquilerManager como un método específico.
        # return self.alquiler_manager.listar_por_cliente(id_cliente)
        pass # Implementación pendiente