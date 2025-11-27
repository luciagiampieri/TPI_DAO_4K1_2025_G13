// FRONTEND/src/pages/Vehiculos/VehiculosList.jsx

import { PencilSquareIcon, TrashIcon } from "@heroicons/react/24/solid";
import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import { 
    listarVehiculos, 
    crearVehiculo, 
    getCategorias, 
    getEstadosPorAmbito, 
    eliminarVehiculo,
    actualizarVehiculo
} from '../../services/vehiculoService';

// ID de Ambito para Vehículos (según tu script SQL, ID_AMBITO = 1 es 'Vehiculo')
const AMBITO_VEHICULO_ID = 1; 

const VehiculosList = () => {
    const [vehiculos, setVehiculos] = useState([]);
    const [categorias, setCategorias] = useState([]);
    const [estados, setEstados] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    // Modal alta
    const [formVisible, setFormVisible] = useState(false);
    // Modal edición
    const [editVisible, setEditVisible] = useState(false);
    const [vehiculoEditando, setVehiculoEditando] = useState(null);
    
    // Estado para el formulario de alta
    const [nuevoVehiculo, setNuevoVehiculo] = useState({
        modelo: '',
        anio: '',
        categoriaId: '',
        estadoId: '', // Necesario para la FK y para inicializar
        patente: '',
        kilometraje: 0,
        costoDiario: ''
    });

    // =========================================
    // Carga inicial: categorías, estados, lista
    // =========================================
    const loadInitialData = async () => {
        try {
            const [cats, ests, vehs] = await Promise.all([
                getCategorias(),
                getEstadosPorAmbito(AMBITO_VEHICULO_ID),
                listarVehiculos()
            ]);
            
            setCategorias(cats);
            setEstados(ests);
            setVehiculos(vehs);

            // Establecer el estado inicial (ej: Disponible) por defecto
            const disponible = ests.find(e => e.nombre === 'Disponible');
            if (disponible) {
                setNuevoVehiculo(prev => ({ ...prev, estadoId: disponible.id }));
            }

        } catch (error) {
            console.error("Error al cargar datos:", error);
            Swal.fire('Error', 'No se pudieron cargar Categorías o Estados.', 'error');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadInitialData();
    }, []);

    // Solo afecta al formulario de ALTA
    const handleInputChange = (e) => {
        setNuevoVehiculo({ ...nuevoVehiculo, [e.target.name]: e.target.value });
    };

    // Recargar SOLO lista de vehículos (sin tocar categorías/estados)
    const cargarVehiculos = async () => {
        try {
            const data = await listarVehiculos();
            setVehiculos(data);
        } catch (error) {
            console.error("Error al recargar vehículos:", error);
            Swal.fire('Error', 'No se pudieron recargar los vehículos.', 'error');
        }
    };

    // ======================
    //   ELIMINAR VEHÍCULO
    // ======================
    const handleDeleteVehiculo = async (id, patente) => {
        const result = await Swal.fire({
            title: `¿Estás seguro de eliminar el vehículo ${patente}?`,
            text: "Esta acción no se puede deshacer.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        });

        if (result.isConfirmed) {
            try {
                await eliminarVehiculo(id);
                Swal.fire('Eliminado!', `El vehículo ${patente} ha sido eliminado.`, 'success');
                cargarVehiculos();
            } catch (error) {
                const errorMessage = error.response?.data?.error || "Error al eliminar (posiblemente tiene alquileres asociados).";
                Swal.fire('Error', errorMessage, 'error');
            }
        }
    };

    // ======================
    //   CREAR VEHÍCULO
    // ======================
    const handleCreateVehiculo = async (e) => {
        e.preventDefault();
        try {
            await crearVehiculo(nuevoVehiculo);
            Swal.fire('¡Éxito!', 'Vehículo registrado correctamente.', 'success');
            setFormVisible(false);
            setNuevoVehiculo({
                modelo: '',
                anio: '',
                categoriaId: '',
                estadoId: estados.find(e => e.nombre === 'Disponible')?.id || '',
                patente: '',
                kilometraje: 0,
                costoDiario: ''
            });
            cargarVehiculos();

            loadInitialData(); // Recarga la tabla

        } catch (error) {
            Swal.fire('Error', error.response?.data?.error || 'Hubo un problema al registrar.', 'error');
        }
    };

    // ======================
    //   EDITAR VEHÍCULO
    // ======================
    const handleEditVehiculo = (vehiculo) => {
        setVehiculoEditando({
            id: vehiculo.id,
            modelo: vehiculo.modelo,
            anio: vehiculo.anio,
            categoriaId: categorias.find(c => c.nombre === vehiculo.categoria)?.id || "",
            patente: vehiculo.patente,
            costoDiario: vehiculo.costo_diario,
            estadoId: estados.find(e => e.nombre === vehiculo.estado)?.id || "",
            kilometraje: vehiculo.kilometraje
        });
        setEditVisible(true);
    };

    const handleUpdateVehiculo = async (e) => {
        e.preventDefault();
        try {
            await actualizarVehiculo(vehiculoEditando.id, vehiculoEditando);
            Swal.fire("Éxito", "Vehículo actualizado correctamente", "success");
            setEditVisible(false);
            setVehiculoEditando(null);
            cargarVehiculos();
        } catch (error) {
            const msg = error.response?.data?.error || 'No se pudo actualizar el vehículo.';
            Swal.fire("Error", msg, "error");
        }
    };

    if (isLoading) {
        return <div className="text-center p-10 text-lg text-blue-600 font-semibold">Cargando vehículos y configuración...</div>;
    }

    // Función para obtener estilo según estado
        const getEstadoStyle = (estado) => {
            switch (estado) {
                case 'En Mantenimiento': return 'bg-blue-100 text-blue-800';
                case 'Alquilado': return 'bg-red-100 text-red-800';
                case 'Disponible': return 'bg-green-100 text-green-800';
                default: return 'bg-gray-100 text-gray-800';
            }
        };

    return (
        <div>
            {/* ENCABEZADO */}
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-gray-800">ABM de Vehículos</h2>
                <button
                    onClick={() => setFormVisible(true)}
                    className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg shadow-md"
                >
                    + Nuevo Vehículo
                </button>
            </div>

            {/* MODAL ALTA VEHÍCULO */}
            {formVisible && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl shadow-2xl w-full max-w-lg">
                        <h3 className="text-2xl font-semibold mb-4 border-b pb-2">Registrar Nuevo Vehículo</h3>
                        <form onSubmit={handleCreateVehiculo} className="space-y-4">
                            
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-gray-700 text-sm font-medium">Modelo</label>
                                    <input 
                                        type="text" 
                                        name="modelo" 
                                        value={nuevoVehiculo.modelo} 
                                        onChange={handleInputChange} 
                                        required 
                                        className="w-full mt-1 p-2 border border-gray-300 rounded-lg" 
                                    />
                                </div>
                                <div>
                                    <label className="block text-gray-700 text-sm font-medium">Año</label>
                                    <input 
                                        type="number" 
                                        name="anio" 
                                        value={nuevoVehiculo.anio} 
                                        onChange={handleInputChange} 
                                        required 
                                        className="w-full mt-1 p-2 border border-gray-300 rounded-lg" 
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-gray-700 text-sm font-medium">Categoría</label>
                                <select 
                                    name="categoriaId" 
                                    value={nuevoVehiculo.categoriaId} 
                                    onChange={handleInputChange} 
                                    required 
                                    className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                >
                                    <option value="" disabled>Seleccione Categoría</option>
                                    {categorias.map(cat => (
                                        <option key={cat.id} value={cat.id}>{cat.nombre}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-gray-700 text-sm font-medium">Patente</label>
                                    <input 
                                        type="text" 
                                        name="patente" 
                                        value={nuevoVehiculo.patente} 
                                        onChange={handleInputChange} 
                                        required 
                                        className="w-full mt-1 p-2 border border-gray-300 rounded-lg" 
                                        maxLength="7" 
                                    />
                                </div>
                                <div>
                                    <label className="block text-gray-700 text-sm font-medium">Costo Diario ($)</label>
                                    <input 
                                        type="number" 
                                        name="costoDiario" 
                                        value={nuevoVehiculo.costoDiario} 
                                        onChange={handleInputChange} 
                                        required 
                                        className="w-full mt-1 p-2 border border-gray-300 rounded-lg" 
                                    />
                                </div>
                            </div>
                            
                            {/* Estado inicial oculto */}
                            <div className='hidden'>
                                <label className="block text-gray-700 text-sm font-medium">Estado Inicial</label>
                                <select 
                                    name="estadoId" 
                                    value={nuevoVehiculo.estadoId} 
                                    onChange={handleInputChange} 
                                    className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                >
                                    {estados.map(est => (
                                        <option key={est.id} value={est.id}>{est.nombre}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="flex justify-end pt-4 space-x-3">
                                <button 
                                    type="button" 
                                    onClick={() => setFormVisible(false)} 
                                    className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                                >
                                    Cancelar
                                </button>
                                <button 
                                    type="submit" 
                                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                                >
                                    Guardar Vehículo
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* MODAL EDICIÓN VEHÍCULO */}
            {editVisible && vehiculoEditando && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl shadow-2xl w-full max-w-lg">
                        <h3 className="text-2xl font-semibold mb-4 border-b pb-2">Editar Vehículo</h3>

                        <form onSubmit={handleUpdateVehiculo} className="space-y-4">

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-gray-700 text-sm font-medium">Modelo</label>
                                    <input 
                                        type="text"
                                        value={vehiculoEditando.modelo}
                                        onChange={e => setVehiculoEditando({ ...vehiculoEditando, modelo: e.target.value })}
                                        className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                    />
                                </div>
                                <div>
                                    <label className="block text-gray-700 text-sm font-medium">Año</label>
                                    <input 
                                        type="number"
                                        value={vehiculoEditando.anio}
                                        onChange={e => setVehiculoEditando({ ...vehiculoEditando, anio: e.target.value })}
                                        className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-gray-700 text-sm font-medium">Categoría</label>
                                <select
                                    value={vehiculoEditando.categoriaId}
                                    onChange={e => setVehiculoEditando({ ...vehiculoEditando, categoriaId: e.target.value })}
                                    className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                >
                                    {categorias.map(cat => (
                                        <option key={cat.id} value={cat.id}>{cat.nombre}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-gray-700 text-sm font-medium">Patente</label>
                                    <input 
                                        type="text"
                                        value={vehiculoEditando.patente}
                                        onChange={e => setVehiculoEditando({ ...vehiculoEditando, patente: e.target.value })}
                                        className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-700 text-sm font-medium">Costo Diario ($)</label>
                                    <input 
                                        type="number"
                                        value={vehiculoEditando.costoDiario}
                                        onChange={e => setVehiculoEditando({ ...vehiculoEditando, costoDiario: e.target.value })}
                                        className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-gray-700 text-sm font-medium">Kilometraje</label>
                                <input 
                                    type="number"
                                    value={vehiculoEditando.kilometraje}
                                    onChange={e => setVehiculoEditando({ ...vehiculoEditando, kilometraje: e.target.value })}
                                    className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                />
                            </div>

                            <div>
                                <label className="block text-gray-700 text-sm font-medium">Estado</label>
                                <select
                                    value={vehiculoEditando.estadoId}
                                    onChange={e => setVehiculoEditando({ ...vehiculoEditando, estadoId: e.target.value })}
                                    className="w-full mt-1 p-2 border border-gray-300 rounded-lg"
                                >
                                    {estados.map(est => (
                                        <option key={est.id} value={est.id}>{est.nombre}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="flex justify-end pt-4 space-x-3">
                                <button 
                                    type="button" 
                                    onClick={() => { setEditVisible(false); setVehiculoEditando(null); }} 
                                    className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-lg"
                                >
                                    Cancelar
                                </button>
                                <button 
                                    type="submit" 
                                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg"
                                >
                                    Guardar Cambios
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* TABLA DE LISTADO DE VEHÍCULOS */}
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
                <h3 className="text-xl font-semibold mb-4">Vehículos Registrados ({vehiculos.length})</h3>
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Patente</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Modelo / Año</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoría</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Costo Diario</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                            <th className="px-6 py-3"></th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {vehiculos.length > 0 ? (
                            vehiculos.map((v) => {
                                return (
                                    <tr key={v.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{v.patente}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{v.modelo} / {v.anio}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{v.categoria}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${v.costo_diario}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getEstadoStyle(v.estado)}`}>
                                                {v.estado}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <div className="flex justify-end gap-4">
                                                {/* EDITAR */}
                                                <button
                                                    onClick={() => handleEditVehiculo(v)}
                                                    className="text-blue-600 hover:text-blue-800"
                                                    title="Editar"
                                                >
                                                    <PencilSquareIcon className="h-6 w-6" />
                                                </button>

                                                {/* ELIMINAR */}
                                                <button
                                                    onClick={() => handleDeleteVehiculo(v.id, v.patente)}
                                                    className="text-red-600 hover:text-red-800"
                                                    title="Eliminar"
                                                >
                                                    <TrashIcon className="h-6 w-6" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                );
                            })
                        ) : (
                            <tr>
                                <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                                    No hay vehículos registrados. ¡Usa el botón "Nuevo Vehículo" para dar de alta!
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default VehiculosList;
