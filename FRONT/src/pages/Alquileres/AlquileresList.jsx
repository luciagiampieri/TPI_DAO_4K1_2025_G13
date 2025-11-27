import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import { getAlquileres, crearAlquiler, getEmpleados } from '../../services/alquilerService';
import { getClientes } from '../../services/clienteService';
import { listarVehiculos } from '../../services/vehiculoService';

const AlquileresList = () => {
    const [alquileres, setAlquileres] = useState([]);
    // Listas para los dropdowns
    const [clientes, setClientes] = useState([]);
    const [vehiculos, setVehiculos] = useState([]);
    const [empleados, setEmpleados] = useState([]);
    
    const [isLoading, setIsLoading] = useState(true);
    const [formVisible, setFormVisible] = useState(false);

    // Estado del formulario
    const [nuevoAlquiler, setNuevoAlquiler] = useState({
        clienteId: '',
        vehiculoId: '',
        empleadoId: '',
        fechaInicio: '', // Formato para input datetime-local: YYYY-MM-DDTHH:mm
        fechaFin: ''
    });

    // Función de carga de datos (Definida fuera de useEffect para reusar)
    const loadData = async () => {
        setIsLoading(true);
        try {
            const [alqData, cliData, vehData, empData] = await Promise.all([
                getAlquileres(),
                getClientes(),
                listarVehiculos(),
                getEmpleados()
            ]);
            setAlquileres(alqData);
            setClientes(cliData);
            setVehiculos(vehData);
            setEmpleados(empData);
        } catch (error) {
            console.error("Error cargando datos:", error);
            Swal.fire('Error', 'No se pudo cargar la información inicial.', 'error');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const handleInputChange = (e) => {
        setNuevoAlquiler({ ...nuevoAlquiler, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Validación básica de fechas en el front
        if (new Date(nuevoAlquiler.fechaInicio) >= new Date(nuevoAlquiler.fechaFin)) {
            Swal.fire('Error', 'La fecha de fin debe ser posterior al inicio.', 'warning');
            return;
        }

        try {
            await crearAlquiler(nuevoAlquiler);
            Swal.fire('¡Registrado!', 'El alquiler se ha creado con éxito.', 'success');
            setFormVisible(false);
            setNuevoAlquiler({ clienteId: '', vehiculoId: '', empleadoId: '', fechaInicio: '', fechaFin: '' });
            loadData(); // Recargar tabla para ver el nuevo alquiler y actualizar disponibilidad
        } catch (error) {
            const msg = error.response?.data?.error || 'Error al registrar el alquiler.';
            Swal.fire('Error', msg, 'error');
        }
    };

    // Función para obtener estilo según estado
    const getEstadoStyle = (estado) => {
        switch (estado) {
            case 'Pendiente de inicio': return 'bg-blue-100 text-blue-800';
            case 'En curso': return 'bg-green-100 text-green-800';
            case 'Finalizado': return 'bg-red-100 text-red-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    if (isLoading) return <div className="text-center p-10">Cargando Sistema de Alquileres...</div>;

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-gray-800">Gestión de Alquileres</h2>
                <button
                    onClick={() => setFormVisible(true)}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg shadow-md transition-colors"
                >
                    + Nuevo Alquiler
                </button>
            </div>

            {/* MODAL DE ALTA */}
            {formVisible && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl shadow-2xl w-full max-w-2xl">
                        <h3 className="text-2xl font-semibold mb-4 border-b pb-2">Registrar Alquiler</h3>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {/* Cliente */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Cliente</label>
                                    <select name="clienteId" value={nuevoAlquiler.clienteId} onChange={handleInputChange} required className="mt-1 block w-full p-2 border border-gray-300 rounded-md">
                                        <option value="">Seleccione Cliente</option>
                                        {clientes.map(c => (
                                            <option key={c.id} value={c.id}>{c.nombre} (DNI: {c.dni})</option>
                                        ))}
                                    </select>
                                </div>

                                {/* Vehículo */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Vehículo</label>
                                    <select name="vehiculoId" value={nuevoAlquiler.vehiculoId} onChange={handleInputChange} required className="mt-1 block w-full p-2 border border-gray-300 rounded-md">
                                        <option value="">Seleccione Vehículo</option>
                                        {vehiculos.map(v => (
                                            <option key={v.id} value={v.id}>
                                                {v.patente} - {v.modelo} (${v.costo_diario}/día)
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {/* Fechas */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Fecha Inicio</label>
                                    <input type="datetime-local" name="fechaInicio" value={nuevoAlquiler.fechaInicio} onChange={handleInputChange} required className="mt-1 block w-full p-2 border border-gray-300 rounded-md" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Fecha Fin</label>
                                    <input type="datetime-local" name="fechaFin" value={nuevoAlquiler.fechaFin} onChange={handleInputChange} required className="mt-1 block w-full p-2 border border-gray-300 rounded-md" />
                                </div>
                            </div>

                            {/* Empleado */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Empleado Responsable</label>
                                <select name="empleadoId" value={nuevoAlquiler.empleadoId} onChange={handleInputChange} required className="mt-1 block w-full p-2 border border-gray-300 rounded-md">
                                    <option value="">Seleccione Empleado</option>
                                    {empleados.map(e => (
                                        <option key={e.id} value={e.id}>{e.nombre}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="flex justify-end pt-4 space-x-3">
                                <button type="button" onClick={() => setFormVisible(false)} className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-lg">
                                    Cancelar
                                </button>
                                <button type="submit" className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg">
                                    Confirmar Alquiler
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* TABLA */}
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vehículo</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fechas</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Estimado</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {alquileres.map((a) => (
                            <tr key={a.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{a.id}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{a.vehiculo}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{a.cliente}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    <div className="text-xs">In: {a.fecha_inicio}</div>
                                    <div className="text-xs">Out: {a.fecha_fin}</div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">${a.costo_total}</td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getEstadoStyle(a.estado)}`}>
                                        {a.estado}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {alquileres.length === 0 && (
                    <div className="text-center py-10 text-gray-500">No hay alquileres registrados.</div>
                )}
            </div>
        </div>
    );
};

export default AlquileresList;