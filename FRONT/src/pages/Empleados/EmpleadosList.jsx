import React, { useEffect, useState } from 'react';
import { getEmpleados, createEmpleado, updateEmpleado, deleteEmpleado } from '../../services/empleadoService';
import Swal from 'sweetalert2';
import { PencilSquareIcon, TrashIcon, UserPlusIcon, IdentificationIcon } from "@heroicons/react/24/solid";

const EmpleadosList = () => {
    const [empleados, setEmpleados] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    // --- Alta ---
    const [formVisible, setFormVisible] = useState(false);
    const [nuevoEmpleado, setNuevoEmpleado] = useState({ nombre: '', dni: '', mail: '' });

    // --- Edición ---
    const [editVisible, setEditVisible] = useState(false);
    const [empleadoEditando, setEmpleadoEditando] = useState(null);

    useEffect(() => {
        cargarEmpleados();
    }, []);

    const cargarEmpleados = async () => {
        setIsLoading(true);
        try {
            const data = await getEmpleados();
            setEmpleados(data);
        } catch (error) {
            Swal.fire("Error", "No se pudieron cargar los empleados", "error");
        } finally {
            setIsLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        if (editVisible) {
            setEmpleadoEditando({ ...empleadoEditando, [name]: value });
        } else {
            setNuevoEmpleado({ ...nuevoEmpleado, [name]: value });
        }
    };

    // --- Crear ---
    const handleCreateEmpleado = async (e) => {
        e.preventDefault();
        try {
            await createEmpleado(nuevoEmpleado);
            Swal.fire('¡Éxito!', 'Empleado registrado correctamente.', 'success');
            setFormVisible(false);
            setNuevoEmpleado({ nombre: '', dni: '', mail: '' });
            cargarEmpleados();
        } catch (error) {
            Swal.fire('Error', error.response?.data?.error || 'Hubo un problema.', 'error');
        }
    };

    // --- Editar ---
    const handleEditClick = (emp) => {
        setEmpleadoEditando({ ...emp });
        setEditVisible(true);
    };

    const handleUpdateEmpleado = async (e) => {
        e.preventDefault();
        try {
            await updateEmpleado(empleadoEditando.id, empleadoEditando);
            Swal.fire('Actualizado', 'Datos del empleado actualizados.', 'success');
            setEditVisible(false);
            setEmpleadoEditando(null);
            cargarEmpleados();
        } catch (error) {
            Swal.fire('Error', 'No se pudo actualizar.', 'error');
        }
    };

    // --- Eliminar ---
    const handleDeleteEmpleado = async (id, nombre) => {
        const result = await Swal.fire({
            title: `¿Eliminar a ${nombre}?`,
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
                await deleteEmpleado(id);
                Swal.fire("Eliminado", "El empleado ha sido eliminado.", "success");
                cargarEmpleados();
            } catch (error) {
                Swal.fire("Error", "No se pudo eliminar (posiblemente tenga alquileres asociados).", "error");
            }
        }
    };

    if (isLoading) 
        return <div className="text-center p-10">Cargando empleados...</div>;

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
                    <IdentificationIcon className="h-8 w-8 text-sky-600" />
                    Gestión de Empleados
                </h2>
                <button
                    onClick={() => setFormVisible(true)}
                    className="bg-sky-600 hover:bg-sky-700 text-white font-bold py-2 px-4 rounded-lg shadow-md flex items-center gap-2 transition-colors"
                >
                    <UserPlusIcon className="h-5 w-5" />
                    Nuevo Empleado
                </button>
            </div>

            {/* TABLA */}
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">DNI</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                            <th className="px-6 py-3 text-right">Acciones</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {empleados.map(emp => (
                            <tr key={emp.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 text-sm text-gray-500">#{emp.id}</td>
                                <td className="px-6 py-4 text-sm font-medium text-gray-900">{emp.nombre}</td>
                                <td className="px-6 py-4 text-sm text-gray-500">{emp.dni}</td>
                                <td className="px-6 py-4 text-sm text-gray-500">{emp.mail}</td>
                                <td className="px-6 py-4 text-right flex justify-end gap-3">
                                    <button onClick={() => handleEditClick(emp)} className="text-blue-600 hover:text-blue-800" title="Editar">
                                        <PencilSquareIcon className="h-5 w-5" />
                                    </button>
                                    <button onClick={() => handleDeleteEmpleado(emp.id, emp.nombre)} className="text-red-600 hover:text-red-800" title="Eliminar">
                                        <TrashIcon className="h-5 w-5" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {empleados.length === 0 && <div className="text-center p-6 text-gray-500">No hay empleados registrados.</div>}
            </div>

            {/* MODAL ALTA */}
            {formVisible && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl w-full max-w-md shadow-2xl">
                        <h3 className="text-xl font-bold mb-4 text-gray-800">Nuevo Empleado</h3>
                        <form onSubmit={handleCreateEmpleado} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Nombre Completo</label>
                                <input type="text" name="nombre" value={nuevoEmpleado.nombre} onChange={handleInputChange} required className="w-full border rounded-lg p-2 mt-1" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">DNI</label>
                                <input type="text" name="dni" value={nuevoEmpleado.dni} onChange={handleInputChange} required className="w-full border rounded-lg p-2 mt-1" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Email</label>
                                <input type="email" name="mail" value={nuevoEmpleado.mail} onChange={handleInputChange} className="w-full border rounded-lg p-2 mt-1" />
                            </div>
                            <div className="flex justify-end gap-3 pt-2">
                                <button type="button" onClick={() => setFormVisible(false)} className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300">Cancelar</button>
                                <button type="submit" className="bg-sky-600 text-white px-4 py-2 rounded-lg hover:bg-sky-700">Guardar</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* MODAL EDICIÓN */}
            {editVisible && empleadoEditando && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl w-full max-w-md shadow-2xl">
                        <h3 className="text-xl font-bold mb-4 text-gray-800">Editar Empleado</h3>
                        <form onSubmit={handleUpdateEmpleado} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Nombre</label>
                                <input type="text" name="nombre" value={empleadoEditando.nombre} onChange={handleInputChange} required className="w-full border rounded-lg p-2 mt-1" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">DNI</label>
                                <input type="text" name="dni" value={empleadoEditando.dni} onChange={handleInputChange} required className="w-full border rounded-lg p-2 mt-1" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Email</label>
                                <input type="email" name="mail" value={empleadoEditando.mail} onChange={handleInputChange} className="w-full border rounded-lg p-2 mt-1" />
                            </div>
                            <div className="flex justify-end gap-3 pt-2">
                                <button type="button" onClick={() => setEditVisible(false)} className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300">Cancelar</button>
                                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Actualizar</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default EmpleadosList;