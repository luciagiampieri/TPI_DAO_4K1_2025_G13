import axios from 'axios';

const VEHICULOS_URL = '/api/vehiculos';
const CATEGORIAS_URL = '/api/categoria';
const ESTADOS_URL = '/api/estados';

// --- Funciones de Lookup (Tablas de Consulta) ---

export const getCategorias = async () => {
    // Llama al endpoint /api/categoria
    const response = await axios.get(CATEGORIAS_URL);
    return response.data;
};

export const getEstadosPorAmbito = async (ambitoId) => {
    // Llama al endpoint /api/estados/<int:ambito_id>
    const response = await axios.get(`${ESTADOS_URL}/${ambitoId}`);
    return response.data;
};

// --- Funciones CRUD de Vehículos ---

export const listarVehiculos = async () => {
    // Llama al endpoint /api/vehiculos (GET)
    // Nota: Tu routes.py actual solo tiene un endpoint para obtener 
    // un detalle, NO una lista. Vamos a asumir que tu backend devolverá la lista.
    const response = await axios.get(VEHICULOS_URL); 
    return response.data;
};

export const crearVehiculo = async (vehiculoData) => {
    // Llama al endpoint /api/vehiculos (POST)
    const response = await axios.post(VEHICULOS_URL, vehiculoData);
    if (response.status === 201) {
        return true;
    }
    throw new Error('Error al crear el vehículo');
};

export const eliminarVehiculo = async (idVehiculo) => {
    // Llama al endpoint DELETE /api/vehiculos/{id}
    const response = await axios.delete(`${VEHICULOS_URL}/${idVehiculo}`); 
    return response.data;
};

export const actualizarVehiculo = async (idVehiculo, data) => {
    const response = await axios.put(`${VEHICULOS_URL}/${idVehiculo}`, data);
    return response.data;
};

export const getVehiculoById = async (id) => {
    const response = await axios.get(`${VEHICULOS_URL}/${id}`);
    return response.data;
};

export const getMantenimientosByVehiculo = async (id) => {
    const response = await axios.get(`/api/mantenimientos/vehiculo/${id}`);
    return response.data;
};
