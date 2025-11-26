import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Home/Dashboard';
import React from 'react';
import ClientesList from './pages/Clients/ClientesList';
import VehiculosList from './pages/Vehiculos/VehiculosList';

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
                <Route path="/alquileres" element={<PaginaEnConstruccion titulo="Alquileres" />} />
                <Route path="/reportes" element={<PaginaEnConstruccion titulo="Reportes" />} />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
}

export default App;