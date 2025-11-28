import axios from 'axios';

const API_URL = '/api/incidentes';

export const getTiposIncidente = async () => {
    const response = await axios.get('/api/tipos_incidente');
    return response.data;
};

export const getIncidentesByAlquiler = async (idAlquiler) => {
    const response = await axios.get(`${API_URL}/alquiler/${idAlquiler}`);
    return response.data;
};

export const crearIncidente = async (data) => {
    const response = await axios.post(API_URL, data);
    return response.data;
};

export const eliminarIncidente = async (id) => {
    return await axios.delete(`${API_URL}/${id}`);
};