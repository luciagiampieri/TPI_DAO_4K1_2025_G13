import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAlquilerById } from '../../services/alquilerService';
import { 
    getIncidentesByAlquiler, getTiposIncidente, 
    crearIncidente, eliminarIncidente 
} from '../../services/incidenteService';
import { ArrowLeftIcon, ExclamationTriangleIcon, TrashIcon } from "@heroicons/react/24/solid";
import Swal from 'sweetalert2';

const AlquilerDetalle = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    
    const [alquiler, setAlquiler] = useState(null);
    const [incidentes, setIncidentes] = useState([]);
    const [tiposIncidente, setTiposIncidente] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    // Modal (Solo visibilidad, ya no hay estado de edición)
    const [modalVisible, setModalVisible] = useState(false);
    
    const [formData, setFormData] = useState({
        id_tipo: '', fecha: '', descripcion: ''
    });

    const loadData = async () => {
        try {
            const [alq, inc, tipos] = await Promise.all([
                getAlquilerById(id),
                getIncidentesByAlquiler(id),
                getTiposIncidente()
            ]);
            setAlquiler(alq);
            setIncidentes(inc);
            setTiposIncidente(tipos);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => { loadData(); }, [id]);

    // --- Handlers Modal ---
    const openModalNew = () => {
        setFormData({ id_tipo: '', fecha: '', descripcion: '' });
        setModalVisible(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const payload = { ...formData, id_alquiler: id };
            
            // Solo llamamos a crear
            await crearIncidente(payload);
            
            setModalVisible(false);
            loadData();
            Swal.fire('Éxito', 'Incidente reportado.', 'success');
        } catch (error) {
            Swal.fire('Error', 'Hubo un problema.', 'error');
        }
    };

    const handleDelete = async (idInc) => {
        const res = await Swal.fire({ title: '¿Eliminar?', icon: 'warning', showCancelButton: true, confirmButtonText: 'Sí, borrar' });
        if (res.isConfirmed) {
            try {
                await eliminarIncidente(idInc);
                loadData();
                Swal.fire('Eliminado', '', 'success');
            } catch (e) {
                Swal.fire('Error', 'No se pudo eliminar', 'error');
            }
        }
    };

    if (isLoading) return <div className="p-10 text-center">Cargando...</div>;
    if (!alquiler) return <div className="p-10 text-center">No encontrado</div>;

    return (
        <div className="space-y-6">
            <button onClick={() => navigate('/alquileres')} className="flex items-center text-gray-600 hover:text-blue-600">
                <ArrowLeftIcon className="h-5 w-5 mr-2" /> Volver
            </button>

            {/* DETALLE ALQUILER */}
            <div className="bg-white rounded-xl shadow p-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="col-span-2">
                    <h2 className="text-xl font-bold">{alquiler.vehiculo}</h2>
                    <p className="text-gray-500">Cliente: {alquiler.cliente}</p>
                </div>
                <div>
                    <p className="text-sm text-gray-500">Estado</p>
                    <span className="font-bold text-blue-600">{alquiler.estado}</span>
                </div>
                <div className="col-span-4 text-sm text-gray-600 border-t pt-2 mt-2 flex gap-4">
                    <span><b>Desde:</b> {alquiler.fecha_inicio}</span>
                    <span><b>Hasta:</b> {alquiler.fecha_fin}</span>
                    <span><b>Empleado:</b> {alquiler.empleado}</span>
                </div>
            </div>

            {/* INCIDENTES */}
            <div className="bg-white rounded-xl shadow">
                <div className="px-6 py-4 border-b flex justify-between bg-gray-50">
                    <div className="flex items-center gap-2">
                        <ExclamationTriangleIcon className="h-5 w-5 text-orange-500" />
                        <h3 className="font-bold">Incidentes Reportados</h3>
                    </div>
                    <button onClick={openModalNew} className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 text-sm">
                        + Reportar Incidente
                    </button>
                </div>
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50 text-xs uppercase text-gray-500">
                        <tr>
                            <th className="px-6 py-3 text-left">Fecha</th>
                            <th className="px-6 py-3 text-left">Tipo</th>
                            <th className="px-6 py-3 text-left">Descripción</th>
                            <th className="px-6 py-3"></th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 text-sm">
                        {incidentes.map(i => (
                            <tr key={i.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4">{i.fecha}</td>
                                <td className="px-6 py-4 font-medium">{i.tipo}</td>
                                <td className="px-6 py-4 text-gray-500">{i.descripcion}</td>
                                <td className="px-6 py-4 text-right flex gap-3 justify-end">
                                    {/* SOLO BOTÓN DE ELIMINAR */}
                                    <button onClick={() => handleDelete(i.id)} className="text-red-600"><TrashIcon className="h-5 w-5"/></button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* MODAL */}
            {modalVisible && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl w-full max-w-md shadow-2xl">
                        <h3 className="text-lg font-bold mb-4">Reportar Incidente</h3>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm">Tipo de Incidente</label>
                                <select className="w-full border p-2 rounded" 
                                    value={formData.id_tipo} 
                                    onChange={e => setFormData({...formData, id_tipo: e.target.value})} 
                                    required
                                >
                                    <option value="">Seleccione...</option>
                                    {tiposIncidente.map(t => <option key={t.id} value={t.id}>{t.nombre}</option>)}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm">Fecha y Hora</label>
                                <input type="datetime-local" className="w-full border p-2 rounded" 
                                    value={formData.fecha} 
                                    onChange={e => setFormData({...formData, fecha: e.target.value})} 
                                    required 
                                />
                            </div>
                            <div>
                                <label className="block text-sm">Descripción</label>
                                <textarea className="w-full border p-2 rounded" 
                                    value={formData.descripcion} 
                                    onChange={e => setFormData({...formData, descripcion: e.target.value})} 
                                />
                            </div>
                            <div className="flex justify-end gap-2 pt-2">
                                <button type="button" onClick={() => setModalVisible(false)} className="bg-gray-200 px-4 py-2 rounded">Cancelar</button>
                                <button type="submit" className="bg-red-600 text-white px-4 py-2 rounded">Guardar</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AlquilerDetalle;