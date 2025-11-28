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

export const eliminarAlquiler = async (idAlquiler) => {
    const response = await axios.delete(`${ALQUILERES_URL}/${idAlquiler}`);
    if (response.status == 200 || response.status == 204){
        return true;
    }
    throw new Error('Error al eliminar el alquiler');
};

export const finalizarAlquiler = async (idAlquiler, kmFinal) => {
    const response = await axios.put(`${ALQUILERES_URL}/finalizar/${idAlquiler}`, { km_final: kmFinal });
    if (response.status === 200) {
        return true;
    }
    throw new Error('Error al finalizar el alquiler');
};