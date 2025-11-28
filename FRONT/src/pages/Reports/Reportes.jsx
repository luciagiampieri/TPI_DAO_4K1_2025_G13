import React, { useEffect, useState } from 'react';
import { 
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
    PieChart, Pie, Cell, LineChart, Line
} from 'recharts';
import { getRankingVehiculos, getFacturacionAnual, getReportePeriodo, getHistorialCliente } from '../../services/reporteService';
import { getClientes } from '../../services/clienteService';

// Colores para el gráfico de torta
const COLORS = ['#d80505ff', '#d30a97ff', '#ff960eff', '#fff642ff', '#9834e5ff'];

const Reportes = () => {
    const [anioFacturacion, setAnioFacturacion] = useState(new Date().getFullYear());
    
    // Estados de Datos
    const [rankingData, setRankingData] = useState([]);
    const [facturacionData, setFacturacionData] = useState([]);
    
    // Estado para Reporte de Período (Líneas)
    const [periodoFechas, setPeriodoFechas] = useState({ desde: '2025-01-01', hasta: '2025-12-31' });
    const [lineasData, setLineasData] = useState([]);

    // Estado para Reporte de Cliente (Tabla)
    const [clientesList, setClientesList] = useState([]);
    const [selectedCliente, setSelectedCliente] = useState('');
    const [clienteReporte, setClienteReporte] = useState([]);

    useEffect(() => {
        cargarDatosIniciales();
    }, []);

    const cargarDatosIniciales = async () => {
        try {
            // Cargar Ranking y Clientes para el dropdown
            const [rank, cli] = await Promise.all([
                getRankingVehiculos(),
                getClientes()
            ]);
            
            // Procesar Ranking para el PieChart (recharts necesita name y value)
            const rankFormat = rank.map(r => ({
                name: r.MODELO,
                value: r.CANTIDAD
            }));
            setRankingData(rankFormat);
            setClientesList(cli);

            // Cargar Facturación por defecto
            cargarFacturacion(anioFacturacion);
            
            // Cargar gráfico de líneas por defecto
            cargarGraficoLineas();

        } catch (error) {
            console.error("Error cargando reportes:", error);
        }
    };

    // --- 1. Lógica Facturación (Barras) ---
    const cargarFacturacion = async (anio) => {
        const data = await getFacturacionAnual(anio);
        setFacturacionData(data);
    };

    // --- 2. Lógica Período (Líneas) ---
    // El backend devuelve una lista de alquileres raw. 
    // Aquí los agrupamos por MES para el gráfico de líneas.
    const cargarGraficoLineas = async (e) => {
        if(e) e.preventDefault();
        const rawData = await getReportePeriodo(periodoFechas.desde, periodoFechas.hasta);
        
        // Agrupación simple por mes (YYYY-MM)
        const agrupado = {};
        rawData.forEach(item => {
            const fecha = item.FEC_INICIO.substring(0, 7); // "2025-01"
            agrupado[fecha] = (agrupado[fecha] || 0) + 1;
        });

        // Convertir a array para Recharts
        const chartData = Object.keys(agrupado).sort().map(key => ({
            fecha: key,
            cantidad: agrupado[key]
        }));
        
        setLineasData(chartData);
    };

    // --- 3. Lógica Cliente (Tabla) ---
    const handleClienteChange = async (e) => {
        const id = e.target.value;
        setSelectedCliente(id);
        if (id) {
            const data = await getHistorialCliente(id);
            setClienteReporte(data);
        } else {
            setClienteReporte([]);
        }
    };

    // --- HELPERS DE FORMATO (Para que se vea lindo) ---
    
    // Formato de moneda para Tooltips y Tablas ($ 1.500.000)
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('es-AR', { 
            style: 'currency', 
            currency: 'ARS', 
            minimumFractionDigits: 0,
            maximumFractionDigits: 0 
        }).format(value);
    };

    // Formato resumido para el Eje Y (1M, 500k, etc)
    const formatYAxis = (value) => {
        if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`;
        if (value >= 1000) return `${(value / 1000).toFixed(0)}k`;
        return value;
    };

    return (
        <div className="space-y-10 pb-10">
            <h1 className="text-3xl font-bold text-gray-800">Tablero de Reportes</h1>

            {/* FILA SUPERIOR: Torta y Barras */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                
                {/* 1. VEHÍCULOS MÁS ALQUILADOS (TORTA) */}
                <div className="bg-white p-6 rounded-xl shadow border border-gray-200">
                    <h3 className="text-lg font-semibold mb-4 text-center">Vehículos más Alquilados</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={rankingData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {rankingData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* 2. FACTURACIÓN MENSUAL (BARRAS) */}
                <div className="bg-white p-6 rounded-xl shadow border border-gray-200">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-semibold">Facturación Mensual</h3>
                        <div className="flex items-center gap-2">
                            <span className="text-sm text-gray-500">Año:</span>
                            <input 
                                type="number" 
                                value={anioFacturacion} 
                                onChange={(e) => {
                                    setAnioFacturacion(e.target.value);
                                    cargarFacturacion(e.target.value);
                                }}
                                className="border rounded p-1 w-20 text-center font-medium text-gray-700"
                            />
                        </div>
                    </div>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={facturacionData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="MES_NOMBRE" axisLine={false} tickLine={false} />
                                {/* Usamos el formateador resumido para el eje Y */}
                                <YAxis 
                                    axisLine={false} 
                                    tickLine={false} 
                                    tickFormatter={formatYAxis} 
                                />
                                {/* Usamos el formateador de moneda completo para el tooltip */}
                                <Tooltip 
                                    formatter={(value) => [formatCurrency(value), "Facturado"]}
                                    cursor={{fill: '#f3f4f6'}}
                                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                                />
                                <Legend />
                                <Bar 
                                    dataKey="TOTAL" 
                                    fill="#0ea5e9" 
                                    name="Total Facturado" 
                                    radius={[4, 4, 0, 0]} 
                                />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* 3. ALQUILERES POR PERÍODO (LÍNEAS) */}
            <div className="bg-white p-6 rounded-xl shadow border border-gray-200">
                <h3 className="text-lg font-semibold mb-4">Tendencia de Alquileres por Período</h3>
                
                <form onSubmit={cargarGraficoLineas} className="flex gap-4 mb-6 items-end">
                    <div>
                        <label className="block text-xs text-gray-500 font-medium mb-1">Desde</label>
                        <input type="date" className="border p-2 rounded text-sm" 
                            value={periodoFechas.desde}
                            onChange={e => setPeriodoFechas({...periodoFechas, desde: e.target.value})} 
                        />
                    </div>
                    <div>
                        <label className="block text-xs text-gray-500 font-medium mb-1">Hasta</label>
                        <input type="date" className="border p-2 rounded text-sm" 
                            value={periodoFechas.hasta}
                            onChange={e => setPeriodoFechas({...periodoFechas, hasta: e.target.value})} 
                        />
                    </div>
                    <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700 transition-colors shadow-sm">
                        Actualizar Gráfico
                    </button>
                </form>

                <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={lineasData}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="fecha" axisLine={false} tickLine={false} />
                            <YAxis allowDecimals={false} axisLine={false} tickLine={false} />
                            <Tooltip 
                                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                            />
                            <Legend />
                            <Line 
                                type="monotone" 
                                dataKey="cantidad" 
                                stroke="#10b981" 
                                name="Cantidad de Alquileres" 
                                strokeWidth={3} 
                                dot={{ r: 4, fill: '#10b981', strokeWidth: 2, stroke: '#fff' }}
                                activeDot={{ r: 6 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* 4. LISTADO DETALLADO POR CLIENTE (TABLA) */}
            <div className="bg-white p-6 rounded-xl shadow border border-gray-200">
                <h3 className="text-lg font-semibold mb-4">Detalle de Alquileres por Cliente</h3>
                
                <div className="mb-4 w-full max-w-md">
                    <select 
                        className="w-full border p-2 rounded focus:ring-2 focus:ring-blue-500 outline-none" 
                        value={selectedCliente} 
                        onChange={handleClienteChange}
                    >
                        <option value="">Seleccione un cliente para ver su historial...</option>
                        {clientesList.map(c => (
                            <option key={c.id} value={c.id}>{c.nombre} (DNI: {c.dni})</option>
                        ))}
                    </select>
                </div>

                {clienteReporte.length > 0 ? (
                    <div className="overflow-x-auto rounded-lg border border-gray-200">
                        <table className="min-w-full divide-y divide-gray-200 text-sm">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase tracking-wider">Fecha Inicio</th>
                                    <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase tracking-wider">Vehículo</th>
                                    <th className="px-4 py-3 text-left font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                                    <th className="px-4 py-3 text-right font-medium text-gray-500 uppercase tracking-wider">Costo Total</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {clienteReporte.map((item, idx) => (
                                    <tr key={idx} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-4 py-3 whitespace-nowrap text-gray-700">{item.FEC_INICIO}</td>
                                        <td className="px-4 py-3 whitespace-nowrap font-medium text-gray-900">{item.PATENTE} - {item.MODELO}</td>
                                        <td className="px-4 py-3 whitespace-nowrap">
                                            <span className={`px-2 py-1 rounded-full text-xs font-bold inline-flex items-center
                                                ${item.ESTADO === 'Finalizado' ? 'bg-green-100 text-green-800' : 
                                                    item.ESTADO === 'En curso' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'}`}>
                                                {item.ESTADO}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 whitespace-nowrap text-right font-bold text-gray-900">
                                            {formatCurrency(item.COSTO_TOTAL)}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <div className="text-gray-500 text-center py-8 bg-gray-50 rounded-lg border border-dashed border-gray-300">
                        {selectedCliente ? "Este cliente no tiene alquileres registrados." : "Seleccione un cliente de la lista para ver su historial."}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Reportes;