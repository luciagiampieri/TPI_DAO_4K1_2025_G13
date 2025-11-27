import axios from 'axios';

const API_URL = '/api/reportes';

// 1. Ranking de Vehículos (Para el gráfico de Torta)
export const getRankingVehiculos = async () => {
    const response = await axios.get(`${API_URL}/ranking`);
    return response.data;
};

// 2. Facturación Mensual (Para el gráfico de Barras)
export const getFacturacionAnual = async (anio) => {
    const response = await axios.get(`${API_URL}/facturacion/${anio}`);
    return response.data;
};

// 3. Alquileres por Período (Para el gráfico de Líneas y tabla)
export const getReportePeriodo = async (desde, hasta) => {
    const response = await axios.post(`${API_URL}/periodo`, { desde, hasta });
    return response.data;
};

// 4. Historial por Cliente (Para el listado detallado)
export const getHistorialCliente = async (idCliente) => {
    const response = await axios.get(`${API_URL}/cliente/${idCliente}`);
    return response.data;
};