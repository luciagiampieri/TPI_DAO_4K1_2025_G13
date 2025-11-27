import React, { useEffect, useState } from 'react';
import { getClientes, createCliente, updateCliente, deleteCliente } from '../../services/clienteService';
import Swal from 'sweetalert2';
import { PencilSquareIcon, TrashIcon } from "@heroicons/react/24/solid";

const ClientesList = () => {
    const [clientes, setClientes] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    // --- Alta ---
    const [formVisible, setFormVisible] = useState(false);
    const [nuevoCliente, setNuevoCliente] = useState({ nombre: '', dni: '', mail: '', telefono: '' });

    // --- Edición ---
    const [editVisible, setEditVisible] = useState(false);
    const [clienteEditando, setClienteEditando] = useState(null);

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
        if (editVisible) {
            setClienteEditando({ ...clienteEditando, [e.target.name]: e.target.value });
        } else {
            setNuevoCliente({ ...nuevoCliente, [e.target.name]: e.target.value });
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
            Swal.fire("Actualizado", "Cliente modificado correctamente", "success");

            setEditVisible(false);
            setClienteEditando(null);

            cargarClientes();
        } catch (error) {
            Swal.fire("Error", error.response?.data?.error || "No se pudo actualizar.", "error");
        }
    };

    // ==========================
    //   ELIMINAR CLIENTE
    // ==========================
    const handleDeleteCliente = async (id, nombre) => {
        const result = await Swal.fire({
            title: `¿Eliminar cliente "${nombre}"?`,
            text: "Esta acción no se puede deshacer.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Sí, eliminar",
            cancelButtonText: "Cancelar"
        });

        if (result.isConfirmed) {
            try {
                await deleteCliente(id);
                Swal.fire("Eliminado", "Cliente eliminado correctamente.", "success");
                cargarClientes();
            } catch (error) {
                Swal.fire("Error", error.response?.data?.error || "No se pudo eliminar.", "error");
            }
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
            {/*   MODAL DE ALTA                */}
            {/* =============================== */}
            {formVisible && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl w-full max-w-md shadow-lg">
                        <h3 className="text-2xl font-semibold mb-4">Registrar Cliente</h3>

                        <form onSubmit={handleCreateCliente}>
                            <div className="mb-4">
                                <label className="block text-gray-700">Nombre</label>
                                <input type="text" name="nombre" value={nuevoCliente.nombre}
                                    onChange={handleInputChange} required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="mb-4">
                                <label className="block text-gray-700">DNI</label>
                                <input type="text" name="dni" value={nuevoCliente.dni}
                                    onChange={handleInputChange} required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="mb-4">
                                <label className="block text-gray-700">Mail</label>
                                <input type="email" name="mail" value={nuevoCliente.mail}
                                    onChange={handleInputChange} className="w-full mt-1 p-2 border rounded-lg" />
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
            {/*   MODAL DE EDICIÓN              */}
            {/* =============================== */}
            {editVisible && clienteEditando && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl w-full max-w-md shadow-lg">
                        <h3 className="text-2xl font-semibold mb-4">Editar Cliente</h3>

                        <form onSubmit={handleUpdateCliente}>
                            <div className="mb-4">
                                <label className="block text-gray-700">Nombre</label>
                                <input type="text" name="nombre"
                                    value={clienteEditando.nombre}
                                    onChange={handleInputChange}
                                    required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="mb-4">
                                <label className="block text-gray-700">DNI</label>
                                <input type="text" name="dni"
                                    value={clienteEditando.dni}
                                    onChange={handleInputChange}
                                    required className="w-full mt-1 p-2 border rounded-lg" />
                            </div>

                            <div className="mb-4">
                                <label className="block text-gray-700">Mail</label>
                                <input type="email" name="mail"
                                    value={clienteEditando.mail}
                                    onChange={handleInputChange}
                                    className="w-full mt-1 p-2 border rounded-lg" />
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
            {/*   TABLA LISTADO                */}
            {/* =============================== */}
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3">ID</th>
                            <th className="px-6 py-3">Nombre</th>
                            <th className="px-6 py-3">DNI</th>
                            <th className="px-6 py-3">Mail</th>
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
                                    <div className="flex justify-end gap-4">

                                        {/* EDITAR */}
                                        <button
                                            onClick={() => handleEditCliente(cliente)}
                                            className="text-blue-600 hover:text-blue-800"
                                            title="Editar"
                                        >
                                            <PencilSquareIcon className="h-6 w-6" />
                                        </button>

                                        {/* ELIMINAR */}
                                        <button
                                            onClick={() => handleDeleteCliente(cliente.id, cliente.nombre)}
                                            className="text-red-600 hover:text-red-800"
                                            title="Eliminar"
                                        >
                                            <TrashIcon className="h-6 w-6" />
                                        </button>

                                    </div>
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