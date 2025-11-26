import React, { useEffect, useState } from 'react';
import { getClientes, createCliente } from '../../services/clienteService';
import Swal from 'sweetalert2'; // Usaremos SweetAlert2

const ClientesList = () => {
    const [clientes, setClientes] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [formVisible, setFormVisible] = useState(false);
    const [nuevoCliente, setNuevoCliente] = useState({ nombre: '', dni: '', mail: '', telefono: '' });

    useEffect(() => {
        cargarClientes();
    }, []);

    const cargarClientes = async () => {
        setIsLoading(true);
        const data = await getClientes();
        setClientes(data);
        setIsLoading(false);
    };

    const handleInputChange = (e) => {
        setNuevoCliente({ ...nuevoCliente, [e.target.name]: e.target.value });
    };

    const handleCreateCliente = async (e) => {
        e.preventDefault();
        try {
            await createCliente(nuevoCliente);
            Swal.fire('¡Éxito!', 'Cliente creado correctamente.', 'success');
            setFormVisible(false);
            setNuevoCliente({ nombre: '', dni: '', mail: '', telefono: '' });
            cargarClientes(); // Recarga la tabla
        } catch (error) {
            Swal.fire('Error', error.response.data.error || 'Hubo un problema.', 'error');
        }
    };

    if (isLoading) {
        return <div className="text-center p-10">Cargando clientes...</div>;
    }

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-gray-800">ABM de Clientes</h2>
                <button
                    onClick={() => setFormVisible(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors shadow-md"
                >
                    + Nuevo Cliente
                </button>
            </div>

            {/* Formulario Modal (ABM) */}
            {formVisible && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl shadow-2xl w-full max-w-md">
                        <h3 className="text-2xl font-semibold mb-4">Registrar Cliente</h3>
                        <form onSubmit={handleCreateCliente}>
                            {/* Inputs */}
                            <div className="mb-4">
                                <label className="block text-gray-700">Nombre</label>
                                <input type="text" name="nombre" value={nuevoCliente.nombre} onChange={handleInputChange} required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>
                            <div className="mb-4">
                                <label className="block text-gray-700">DNI</label>
                                <input type="text" name="dni" value={nuevoCliente.dni} onChange={handleInputChange} required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>
                            <div className="mb-6">
                                <label className="block text-gray-700">Mail</label>
                                <input type="email" name="mail" value={nuevoCliente.mail} onChange={handleInputChange} className="w-full mt-1 p-2 border rounded-lg" />
                            </div>
                            
                            {/* Botones */}
                            <div className="flex justify-end space-x-3">
                                <button type="button" onClick={() => setFormVisible(false)} className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-lg transition-colors">
                                    Cancelar
                                </button>
                                <button type="submit" className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition-colors">
                                    Guardar
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}


            {/* Tabla de Listado */}
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">DNI</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mail</th>
                            <th className="px-6 py-3"></th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {clientes.length > 0 ? (
                            clientes.map((cliente) => (
                                <tr key={cliente.id} className="hover:bg-gray-50">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{cliente.id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{cliente.nombre}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{cliente.dni}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{cliente.mail}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <button className="text-indigo-600 hover:text-indigo-900 mr-2">Editar</button>
                                        <button className="text-red-600 hover:text-red-900">Eliminar</button>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="5" className="px-6 py-4 text-center text-gray-500">
                                    No hay clientes registrados. ¡Agrega uno!
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ClientesList;