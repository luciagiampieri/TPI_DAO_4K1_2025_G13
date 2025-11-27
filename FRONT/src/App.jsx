import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Home/Dashboard';
import React from 'react';
import ClientesList from './pages/Clients/ClientesList';
import VehiculosList from './pages/Vehiculos/VehiculosList';
import AlquileresList from './pages/Alquileres/AlquileresList';
import VehiculoDetalle from './pages/Vehiculos/VehiculoDetalle';

// Placeholder para páginas que aún no creamos
const PaginaEnConstruccion = ({ titulo }) => (
    <div className="p-10 text-center">
        <h2 className="text-2xl font-bold text-gray-400">🚧 {titulo} en construcción 🚧</h2>
    </div>
);

function App() {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/clientes" element={<ClientesList />} />
                <Route path="/vehiculos" element={<VehiculosList />} />
                <Route path="/vehiculos/:id" element={<VehiculoDetalle />} />
                <Route path="/alquileres" element={<AlquileresList />} />
                <Route path="/reportes" element={<PaginaEnConstruccion titulo="Reportes" />} />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
}

export default App;