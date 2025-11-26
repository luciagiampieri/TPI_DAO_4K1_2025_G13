import React from 'react';

const Dashboard = () => {
    return (
        <div>
            <h2 className="text-3xl font-bold text-gray-800 mb-6">Panel de Control</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Tarjeta 1 */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                    <h3 className="text-gray-500 text-sm font-medium">Vehículos Disponibles</h3>
                    <p className="text-4xl font-bold text-gray-800 mt-2">12</p>
                    <span className="text-green-500 text-sm font-medium">+2 esta semana</span>
                </div>

                {/* Tarjeta 2 */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                    <h3 className="text-gray-500 text-sm font-medium">Alquileres Activos</h3>
                    <p className="text-4xl font-bold text-gray-800 mt-2">5</p>
                    <span className="text-blue-500 text-sm font-medium">En curso</span>
                </div>

                {/* Tarjeta 3 */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                    <h3 className="text-gray-500 text-sm font-medium">Ingresos del Mes</h3>
                    <p className="text-4xl font-bold text-gray-800 mt-2">$450k</p>
                    <span className="text-green-500 text-sm font-medium">+15% vs mes pasado</span>
                </div>
            </div>

            {/* Espacio para gráfico o tabla reciente */}
            <div className="mt-8 bg-white p-6 rounded-xl shadow-sm border border-gray-200 h-64 flex items-center justify-center text-gray-400">
                Aquí irían los reportes o últimos movimientos...
            </div>
        </div>
    );
};

export default Dashboard;