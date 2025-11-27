import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getVehiculoById, getMantenimientosByVehiculo } from '../../services/vehiculoService';
import { ArrowLeftIcon, WrenchScrewdriverIcon, PencilSquareIcon, TrashIcon } from "@heroicons/react/24/solid";

const VehiculoDetalle = () => {
    const { id } = useParams(); // Obtiene el ID de la URL
    const navigate = useNavigate();
    
    const [vehiculo, setVehiculo] = useState(null);
    const [mantenimientos, setMantenimientos] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    // Estados del Modal
    const [modalVisible, setModalVisible] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        id_mantenimiento: null,
        id_tipo: '',
        fecha_inicio: '',
        fecha_fin: '',
        costo: '',
        observacion: ''
    });

    const loadData = async () => {
            try {
                const [vehData, mantData] = await Promise.all([
                    getVehiculoById(id),
                    getMantenimientosByVehiculo(id)
                ]);
                setVehiculo(vehData);
                setMantenimientos(mantData);
            } catch (error) {
                console.error("Error cargando detalles:", error);
            } finally {
                setIsLoading(false);
            }
        };

    useEffect(() => {
        loadData();
    }, [id]);

    const openModalNew = () => {
        setFormData({ 
            id_mantenimiento: null, id_tipo: '', fecha_inicio: '', 
            fecha_fin: '', costo: '', observacion: '' 
        });
        setIsEditing(false);
        setModalVisible(true);
    };

    const openModalEdit = (m) => {
        setFormData({
            id_mantenimiento: m.id,
            id_tipo: m.id_tipo, // Asegúrate de que el backend devuelva este ID
            fecha_inicio: m.fecha_inicio, // YYYY-MM-DD
            fecha_fin: m.fecha_fin === 'En curso' ? '' : m.fecha_fin,
            costo: m.costo || '',
            observacion: m.observacion || ''
        });
        setIsEditing(true);
        setModalVisible(true);
    };

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const payload = { ...formData, id_vehiculo: id }; // ID del vehículo actual
            
            if (isEditing) {
                await actualizarMantenimiento(formData.id_mantenimiento, payload);
                Swal.fire('Actualizado', 'Mantenimiento actualizado.', 'success');
            } else {
                await crearMantenimiento(payload);
                Swal.fire('Creado', 'Mantenimiento iniciado.', 'success');
            }
            setModalVisible(false);
            loadData(); // Recarga todo para ver cambios de estado en vehículo
        } catch (error) {
            Swal.fire('Error', 'Hubo un problema.', 'error');
        }
    };

    const handleDelete = async (idMant) => {
        const result = await Swal.fire({
            title: '¿Eliminar registro?', icon: 'warning', showCancelButton: true,
            confirmButtonText: 'Sí, eliminar', confirmButtonColor: '#d33'
        });
        
        if (result.isConfirmed) {
            try {
                await eliminarMantenimiento(idMant);
                Swal.fire('Eliminado', '', 'success');
                loadData();
            } catch (error) {
                Swal.fire('Error', 'No se pudo eliminar.', 'error');
            }
        }
    };

    if (isLoading) return <div className="text-center p-10">Cargando detalles...</div>;
    if (!vehiculo) return <div className="text-center p-10 text-red-500">Vehículo no encontrado</div>;

    return (
        <div className="space-y-6">
            <button onClick={() => navigate('/vehiculos')} className="flex items-center text-gray-600 hover:text-blue-600">
                <ArrowLeftIcon className="h-5 w-5 mr-2" /> Volver
            </button>

            {/* --- DETALLE VEHÍCULO (Igual que antes) --- */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-gray-800">{vehiculo.modelo}</h2>
                    <span className="text-sm text-gray-500">{vehiculo.patente}</span>
                </div>
                <div>
                    <p className="text-sm text-gray-500">Estado</p>
                    <span className={`font-bold ${vehiculo.estado === 'Disponible' ? 'text-green-600' : 'text-orange-500'}`}>
                        {vehiculo.estado}
                    </span>
                </div>
                {/* ... Otros datos ... */}
            </div>

            {/* --- TABLA MANTENIMIENTOS --- */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200">
                <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
                    <div className="flex items-center">
                        <WrenchScrewdriverIcon className="h-5 w-5 text-gray-500 mr-2" />
                        <h3 className="text-lg font-semibold text-gray-800">Historial de Mantenimientos</h3>
                    </div>
                    <button onClick={openModalNew} className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                        + Registrar Mantenimiento
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Inicio</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fin</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Costo</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {mantenimientos.map((m) => (
                                <tr key={m.id} className="hover:bg-gray-50">
                                    <td className="px-6 py-4 text-sm text-gray-900">{m.fecha_inicio}</td>
                                    <td className="px-6 py-4 text-sm">
                                        {m.fecha_fin === 'En curso' ? (
                                            <span className="text-orange-600 font-bold text-xs bg-orange-100 px-2 py-1 rounded-full">En Curso</span>
                                        ) : m.fecha_fin}
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-800">{m.tipo}</td>
                                    <td className="px-6 py-4 text-sm text-gray-900 font-bold">{m.costo ? `$${m.costo}` : '-'}</td>
                                    <td className="px-6 py-4 text-sm flex space-x-3">
                                        <button onClick={() => openModalEdit(m)} className="text-blue-600 hover:text-blue-900" title="Editar / Finalizar">
                                            <PencilSquareIcon className="h-5 w-5" />
                                        </button>
                                        <button onClick={() => handleDelete(m.id)} className="text-red-600 hover:text-red-900" title="Eliminar">
                                            <TrashIcon className="h-5 w-5" />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* --- MODAL FORMULARIO --- */}
            {modalVisible && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl shadow-2xl w-full max-w-md">
                        <h3 className="text-xl font-bold mb-4">{isEditing ? 'Editar / Finalizar' : 'Nuevo Mantenimiento'}</h3>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            
                            {/* Solo mostrar tipo y fecha inicio al crear (o si quieres permitir editar todo, déjalo siempre) */}
                            <div>
                                <label className="block text-sm text-gray-700">Tipo</label>
                                <select name="id_tipo" value={formData.id_tipo} onChange={handleInputChange} className="w-full border rounded p-2" disabled={isEditing}>
                                    <option value="">Seleccione...</option>
                                    {tiposMant.map(t => <option key={t.id} value={t.id}>{t.nombre}</option>)}
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm text-gray-700">Fecha Inicio</label>
                                <input type="date" name="fecha_inicio" value={formData.fecha_inicio} onChange={handleInputChange} className="w-full border rounded p-2" disabled={isEditing} />
                            </div>

                            {/* Solo mostrar Fin y Costo si estamos editando (para finalizar) */}
                            {isEditing && (
                                <>
                                    <div>
                                        <label className="block text-sm text-gray-700">Fecha Fin (Dejar vacío si sigue en curso)</label>
                                        <input type="date" name="fecha_fin" value={formData.fecha_fin} onChange={handleInputChange} className="w-full border rounded p-2" />
                                    </div>
                                    <div>
                                        <label className="block text-sm text-gray-700">Costo ($)</label>
                                        <input type="number" name="costo" value={formData.costo} onChange={handleInputChange} className="w-full border rounded p-2" />
                                    </div>
                                </>
                            )}

                            <div>
                                <label className="block text-sm text-gray-700">Observación</label>
                                <textarea name="observacion" value={formData.observacion} onChange={handleInputChange} className="w-full border rounded p-2" />
                            </div>

                            <div className="flex justify-end space-x-2 pt-4">
                                <button type="button" onClick={() => setModalVisible(false)} className="bg-gray-300 px-4 py-2 rounded">Cancelar</button>
                                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Guardar</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default VehiculoDetalle;