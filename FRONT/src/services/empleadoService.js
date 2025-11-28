import axios from 'axios';

const API_URL = '/api/empleados';

export const getEmpleados = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error("Error al obtener empleados:", error);
        return [];
    }
};

export const createEmpleado = async (empleadoData) => {
    try {
        const response = await axios.post(API_URL, empleadoData);
        return response.data;
    } catch (error) {
        console.error("Error al crear empleado:", error.response?.data);
        throw error;
    }
};

export const updateEmpleado = async (id, empleadoData) => {
    try {
        const response = await axios.put(`${API_URL}/${id}`, empleadoData);
        return response.data;
    } catch (error) {
        console.error("Error al actualizar empleado:", error.response?.data);
        throw error;
    }
};

export const deleteEmpleado = async (id) => {
    try {
        const response = await axios.delete(`${API_URL}/${id}`);
        return response.data;
    } catch (error) {
        console.error("Error al eliminar empleado:", error.response?.data);
        throw error;
    }
};