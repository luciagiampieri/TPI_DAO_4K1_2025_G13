import { Link, useLocation } from 'react-router-dom';
import { HomeIcon, UserGroupIcon, TruckIcon, ClipboardDocumentListIcon, ChartBarIcon } from '@heroicons/react/24/outline';
import React from 'react';

const Sidebar = () => {
    const location = useLocation();

    // Array con las opciones para no repetir código
    const menuItems = [
        { path: '/', name: 'Home', icon: HomeIcon },
        { path: '/clientes', name: 'Clientes', icon: UserGroupIcon },
        { path: '/vehiculos', name: 'Vehículos', icon: TruckIcon },
        { path: '/alquileres', name: 'Alquileres', icon: ClipboardDocumentListIcon },
        { path: '/reportes', name: 'Reportes', icon: ChartBarIcon },
    ];

    return (
        <div className="bg-slate-900 text-white w-64 min-h-screen flex flex-col transition-all duration-300">
            {/* Logo / Título */}
            <div className="h-16 flex items-center justify-center border-b border-slate-700">
                <h1 className="text-2xl font-bold text-blue-500">RentCar<span className="text-white">App</span></h1>
            </div>

            {/* Menú */}
            <nav className="flex-1 px-2 py-4 space-y-2">
                {menuItems.map((item) => {
                    const isActive = location.pathname === item.path;
                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                                isActive 
                                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30' 
                                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                            }`}
                        >
                            <item.icon className="w-6 h-6 mr-3" />
                            <span className="font-medium">{item.name}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Footer del Sidebar */}
            <div className="p-4 border-t border-slate-700">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-sm font-bold">
                        GU
                    </div>
                    <div>
                        <p className="text-sm font-medium">Gestor Usuario</p>
                        <p className="text-xs text-slate-400">Admin</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;