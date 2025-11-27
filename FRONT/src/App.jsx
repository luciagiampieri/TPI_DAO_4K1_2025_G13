import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Home/Dashboard';
import React from 'react';
import ClientesList from './pages/Clients/ClientesList';
import VehiculosList from './pages/Vehiculos/VehiculosList';
import AlquileresList from './pages/Alquileres/AlquileresList';
import VehiculoDetalle from './pages/Vehiculos/VehiculoDetalle';
import Reportes from './pages/Reports/Reportes';


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
                <Route path="/reportes" element={<Reportes />} />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
}

export default App;