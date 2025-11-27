import axios from 'axios';

const API_URL = '/api/mantenimientos';

export const getTiposMantenimiento = async () => {
    const response = await axios.get('/api/tipos_mantenimiento');
    return response.data;
};

export const crearMantenimiento = async (data) => {
    const response = await axios.post(API_URL, data);
    return response.data;
};

export const actualizarMantenimiento = async (id, data) => {
    const response = await axios.put(`${API_URL}/${id}`, data);
    return response.data;
};

export const eliminarMantenimiento = async (id) => {
    const response = await axios.delete(`${API_URL}/${id}`);
    return response.data;
};