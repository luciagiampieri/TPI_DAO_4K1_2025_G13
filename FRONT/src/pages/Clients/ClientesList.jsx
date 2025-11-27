import React, { useEffect, useState } from 'react';
import { getClientes, createCliente, updateCliente } from '../../services/clienteService';
import Swal from 'sweetalert2';

const ClientesList = () => {
    const [clientes, setClientes] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    // Modal alta
    const [formVisible, setFormVisible] = useState(false);

    // Modal edición
    const [editVisible, setEditVisible] = useState(false);
    const [clienteEditando, setClienteEditando] = useState(null);

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
        const { name, value } = e.target;

        if (editVisible) {
            setClienteEditando({ ...clienteEditando, [name]: value });
        } else {
            setNuevoCliente({ ...nuevoCliente, [name]: value });
        }
    };

    // ==========================
    //   CREAR CLIENTE
    // ==========================

    const handleCreateCliente = async (e) => {
        e.preventDefault();
        try {
            await createCliente(nuevoCliente);
            Swal.fire('¡Éxito!', 'Cliente creado correctamente.', 'success');
            
            setFormVisible(false);
            setNuevoCliente({ nombre: '', dni: '', mail: '', telefono: '' });

            cargarClientes();

        } catch (error) {
            Swal.fire('Error', error.response?.data?.error || 'Hubo un problema.', 'error');
        }
    };

    // ==========================
    //   EDITAR CLIENTE
    // ==========================

    const handleEditCliente = (cliente) => {
        setClienteEditando({ ...cliente });
        setEditVisible(true);
    };

    const handleUpdateCliente = async (e) => {
        e.preventDefault();

        try {
            await updateCliente(clienteEditando.id, clienteEditando);
            Swal.fire('¡Actualizado!', 'Cliente modificado correctamente.', 'success');

            setEditVisible(false);
            setClienteEditando(null);
            cargarClientes();

        } catch (error) {
            Swal.fire('Error', error.response?.data?.error || 'No se pudo actualizar.', 'error');
        }
    };


    if (isLoading) {
        return <div className="text-center p-10">Cargando clientes...</div>;
    }

    return (
        <div>
            {/* HEADER */}
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-gray-800">ABM de Clientes</h2>

                <button
                    onClick={() => setFormVisible(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg shadow-md"
                >
                    + Nuevo Cliente
                </button>
            </div>

            {/* =============================== */}
            {/*   MODAL DE ALTA (CREAR CLIENTE) */}
            {/* =============================== */}

            {formVisible && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl w-full max-w-md shadow-lg">

                        <h3 className="text-2xl font-semibold mb-4">Registrar Cliente</h3>

                        <form onSubmit={handleCreateCliente}>
                            {/* Nombre */}
                            <div className="mb-4">
                                <label className="block text-gray-700">Nombre</label>
                                <input type="text" name="nombre" value={nuevoCliente.nombre} onChange={handleInputChange}
                                required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            {/* DNI */}
                            <div className="mb-4">
                                <label className="block text-gray-700">DNI</label>
                                <input type="text" name="dni" value={nuevoCliente.dni} onChange={handleInputChange}
                                required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            {/* Mail */}
                            <div className="mb-4">
                                <label className="block text-gray-700">Mail</label>
                                <input type="email" name="mail" value={nuevoCliente.mail} onChange={handleInputChange}
                                className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            {/* Teléfono */}
                            <div className="mb-4">
                                <label className="block text-gray-700">Teléfono</label>
                                <input type="text" name="telefono" value={nuevoCliente.telefono} onChange={handleInputChange}
                                className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="flex justify-end space-x-3">
                                <button type="button"
                                onClick={() => setFormVisible(false)}
                                className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-lg">
                                    Cancelar
                                </button>

                                <button type="submit"
                                className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg">
                                    Guardar
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* =============================== */}
            {/*   MODAL DE EDICIÓN */}
            {/* =============================== */}

            {editVisible && clienteEditando && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl w-full max-w-md shadow-lg">

                        <h3 className="text-2xl font-semibold mb-4">Editar Cliente</h3>

                        <form onSubmit={handleUpdateCliente}>

                            <div className="mb-4">
                                <label className="block text-gray-700">Nombre</label>
                                <input type="text" name="nombre" value={clienteEditando.nombre}
                                onChange={handleInputChange} required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="mb-4">
                                <label className="block text-gray-700">DNI</label>
                                <input type="text" name="dni" value={clienteEditando.dni}
                                onChange={handleInputChange} required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="mb-4">
                                <label className="block text-gray-700">Mail</label>
                                <input type="email" name="mail" value={clienteEditando.mail}
                                onChange={handleInputChange} className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="mb-4">
                                <label className="block text-gray-700">Teléfono</label>
                                <input type="text" name="telefono" value={clienteEditando.telefono}
                                onChange={handleInputChange} className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="flex justify-end space-x-3">
                                <button type="button"
                                onClick={() => setEditVisible(false)}
                                className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-lg">
                                    Cancelar
                                </button>

                                <button type="submit"
                                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">
                                    Guardar Cambios
                                </button>
                            </div>

                        </form>
                    </div>
                </div>
            )}


            {/* =============================== */}
            {/* TABLA LISTADO */}
            {/* =============================== */}

            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium">Nombre</th>
                            <th className="px-6 py-3 text-left text-xs font-medium">DNI</th>
                            <th className="px-6 py-3 text-left text-xs font-medium">Mail</th>
                            <th className="px-6 py-3"></th>
                        </tr>
                    </thead>

                    <tbody className="bg-white divide-y divide-gray-200">
                        {clientes.map(cliente => (
                            <tr key={cliente.id} className="hover:bg-gray-50">

                                <td className="px-6 py-4">{cliente.id}</td>
                                <td className="px-6 py-4">{cliente.nombre}</td>
                                <td className="px-6 py-4">{cliente.dni}</td>
                                <td className="px-6 py-4">{cliente.mail}</td>

                                <td className="px-6 py-4 text-right">
                                    <button
                                        onClick={() => handleEditCliente(cliente)}
                                        className="text-indigo-600 hover:text-indigo-900 mr-3"
                                    >
                                        Editar
                                    </button>
                                    <button className="text-red-600 hover:text-red-900">Eliminar</button>
                                </td>

                            </tr>
                        ))}
                    </tbody>

                </table>
            </div>
        </div>
    );
};

export default ClientesList;
