// src/pages/Home/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import { 
    TruckIcon, 
    CurrencyDollarIcon, 
    KeyIcon, 
    ClockIcon 
} from '@heroicons/react/24/solid';
import { listarVehiculos } from '../../services/vehiculoService';
import { getAlquileres } from '../../services/alquilerService';

const Dashboard = () => {
    const [stats, setStats] = useState({
        vehiculosDisponibles: 0,
        alquileresActivos: 0,
        ingresosMes: 0
    });
    const [ultimosAlquileres, setUltimosAlquileres] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        cargarDatosDashboard();
    }, []);

    // Cuando se crea un alquiler desde cualquier parte de la app,
    // el Dashboard se refresca automáticamente.
    useEffect(() => {
        const handler = () => {
            cargarDatosDashboard();  // 🔄 refrescar dashboard
        };

        window.addEventListener("alquilerCreado", handler);

        return () => {
            window.removeEventListener("alquilerCreado", handler);
        };
    }, []);

    const cargarDatosDashboard = async () => {
        try {
            // 1. Obtener datos en paralelo
            const [vehiculos, alquileres] = await Promise.all([
                listarVehiculos(),
                getAlquileres()
            ]);

            // --- Lógica de Vehículos Disponibles ---
            // Asumiendo que el estado 'Disponible' viene como string desde tu backend (routes.py)
            const disponibles = vehiculos.filter(v => v.estado === 'Disponible').length;

            // --- Lógica de Alquileres Activos ---
            // Asumiendo que el estado es 'En curso'
            const activos = alquileres.filter(a => a.estado === 'En curso').length;

            // --- Lógica de Ingresos del Mes Actual ---
            const fechaActual = new Date();
            const mesActual = fechaActual.getMonth();
            const anioActual = fechaActual.getFullYear();

            const ingresos = alquileres.reduce((total, alquiler) => {
                // Convertimos la fecha del string (YYYY-MM-DD HH:MM) a objeto Date
                const fechaFin = new Date(alquiler.fecha_fin);
                
                // Sumamos solo si está finalizado y pertenece a este mes/año
                // Nota: Ajusta 'Finalizado' si tu string es diferente
                if (alquiler.estado === 'Finalizado' && 
                    fechaFin.getMonth() === mesActual && 
                    fechaFin.getFullYear() === anioActual) {
                    return total + parseFloat(alquiler.costo_total || 0);
                }
                return total;
            }, 0);

            // --- Lógica de Actividad Reciente (Últimos 5) ---
            // Ordenamos por ID descendente (asumiendo que ID mayor es más nuevo)
            const recientes = [...alquileres]
                .sort((a, b) => b.id - a.id)
                .slice(0, 5);

            setStats({
                vehiculosDisponibles: disponibles,
                alquileresActivos: activos,
                ingresosMes: ingresos
            });
            setUltimosAlquileres(recientes);

        } catch (error) {
            console.error("Error cargando dashboard:", error);
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoading) {
        return <div className="p-8 text-center text-gray-500">Calculando estadísticas...</div>;
    }

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold text-gray-800">Panel de Control</h2>
                <p className="text-gray-500">Resumen operativo de Formula Car</p>
            </div>
            
            {/* --- TARJETAS DE KPI --- */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                
                {/* Vehículos Disponibles */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center justify-between hover:shadow-md transition-shadow">
                    <div>
                        <p className="text-gray-500 text-sm font-medium uppercase tracking-wider">Vehículos Libres</p>
                        <p className="text-4xl font-bold text-gray-800 mt-2">{stats.vehiculosDisponibles}</p>
                        <span className="text-green-600 text-xs font-semibold bg-green-100 px-2 py-1 rounded-full mt-2 inline-block">
                            Listos para alquilar
                        </span>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-full">
                        <TruckIcon className="w-8 h-8 text-blue-600" />
                    </div>
                </div>

                {/* Alquileres Activos */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center justify-between hover:shadow-md transition-shadow">
                    <div>
                        <p className="text-gray-500 text-sm font-medium uppercase tracking-wider">Alquileres en Curso</p>
                        <p className="text-4xl font-bold text-gray-800 mt-2">{stats.alquileresActivos}</p>
                        <span className="text-blue-600 text-xs font-semibold bg-blue-100 px-2 py-1 rounded-full mt-2 inline-block">
                            Actualmente en calle
                        </span>
                    </div>
                    <div className="bg-orange-50 p-4 rounded-full">
                        <KeyIcon className="w-8 h-8 text-orange-600" />
                    </div>
                </div>

                {/* Ingresos Mes */}
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center justify-between hover:shadow-md transition-shadow">
                    <div>
                        <p className="text-gray-500 text-sm font-medium uppercase tracking-wider">Facturado (Mes)</p>
                        <p className="text-4xl font-bold text-gray-800 mt-2">
                            ${stats.ingresosMes.toLocaleString()}
                        </p>
                        <span className="text-gray-400 text-xs mt-2 inline-block">
                            Alquileres finalizados este mes
                        </span>
                    </div>
                    <div className="bg-green-50 p-4 rounded-full">
                        <CurrencyDollarIcon className="w-8 h-8 text-green-600" />
                    </div>
                </div>
            </div>

            {/* --- NUEVA SECCIÓN: ACTIVIDAD RECIENTE --- */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                    <h3 className="font-bold text-gray-700 flex items-center gap-2">
                        <ClockIcon className="w-5 h-5 text-gray-400" />
                        Últimos Movimientos
                    </h3>
                </div>
                
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm text-gray-600">
                        <thead className="bg-gray-50 text-xs uppercase font-medium text-gray-500">
                            <tr>
                                <th className="px-6 py-3">Vehículo</th>
                                <th className="px-6 py-3">Cliente</th>
                                <th className="px-6 py-3">Fecha Inicio</th>
                                <th className="px-6 py-3">Estado</th>
                                <th className="px-6 py-3 text-right">Total</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {ultimosAlquileres.length > 0 ? (
                                ultimosAlquileres.map((alq) => (
                                    <tr key={alq.id} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-6 py-4 font-medium text-gray-800">
                                            {alq.vehiculo}
                                        </td>
                                        <td className="px-6 py-4">{alq.cliente}</td>
                                        <td className="px-6 py-4">{alq.fecha_inicio}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                                                alq.estado === 'En curso' ? 'bg-blue-100 text-blue-700' :
                                                alq.estado === 'Finalizado' ? 'bg-green-100 text-green-700' :
                                                'bg-gray-100 text-gray-600'
                                            }`}>
                                                {alq.estado}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-right font-bold text-gray-800">
                                            ${alq.costo_total}
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="5" className="px-6 py-8 text-center text-gray-400">
                                        No hay actividad reciente registrada.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;