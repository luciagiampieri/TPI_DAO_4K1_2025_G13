import axios from 'axios';

const ALQUILERES_URL = '/api/alquileres';
const EMPLEADOS_URL = '/api/empleados';

export const getAlquileres = async () => {
    const response = await axios.get(ALQUILERES_URL);
    return response.data;
};

export const getEmpleados = async () => {
    const response = await axios.get(EMPLEADOS_URL);
    return response.data;
};

export const crearAlquiler = async (alquilerData) => {
    const response = await axios.post(ALQUILERES_URL, alquilerData);
    window.dispatchEvent(new Event("alquilerCreado"));
    return response.data;
};

export const updateAlquiler = async (id, alquilerData) => {
    const response = await axios.put(`${ALQUILERES_URL}/${id}`, alquilerData);
    window.dispatchEvent(new Event("alquilerCreado"));
    return response.data;
};

export const cancelarAlquiler = async (idAlquiler) => {
    // Apunta a la nueva ruta corregida
    const response = await axios.put(`${ALQUILERES_URL}/cancelar/${idAlquiler}`);
    window.dispatchEvent(new Event("alquilerCreado"));
    return response.data;
};

export const finalizarAlquiler = async (idAlquiler, kmFinal) => {
    const response = await axios.put(`${ALQUILERES_URL}/finalizar/${idAlquiler}`, { 
        kilometrajeFinal: kmFinal 
    });
    if (response.status === 200) {
        return true;
    }
    throw new Error('Error al finalizar el alquiler');
};