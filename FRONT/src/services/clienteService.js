import axios from 'axios';
// Asumimos que el proxy de Vite en vite.config.js apunta a Flask

const API_URL = '/api/clientes'; 

export const getClientes = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error("Error al obtener clientes:", error);
        return [];
    }
};

export const createCliente = async (clienteData) => {
    try {
        const response = await axios.post(API_URL, clienteData);
        return response.data;
    } catch (error) {
        console.error("Error al crear cliente:", error.response.data);
        throw error;
    }
};