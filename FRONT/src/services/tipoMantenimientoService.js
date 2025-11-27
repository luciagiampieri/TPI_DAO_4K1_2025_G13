import axios from 'axios';
// Asumimos que el proxy de Vite en vite.config.js apunta a Flask

const API_URL = '/api/tipos-mantenimiento';

export const getTiposMantenimiento = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error("Error al obtener tipos de mantenimiento:", error);
        return [];
    }
};

export const createTipoMantenimiento = async (tipoMantenimientoData) => {
    try {
        const response = await axios.post(API_URL, tipoMantenimientoData);
        return response.data;
    } catch (error) {
        console.error("Error al crear tipo de mantenimiento:", error.response.data);
        throw error;
    }
};