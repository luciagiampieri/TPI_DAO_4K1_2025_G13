import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import { 
    getAlquileres, 
    crearAlquiler, 
    updateAlquiler, 
    getEmpleados, 
    cancelarAlquiler,  // <--- Usamos cancelar
    finalizarAlquiler 
} from '../../services/alquilerService';
import { getClientes } from '../../services/clienteService';
import { listarVehiculos } from '../../services/vehiculoService';
import { 
    FunnelIcon, 
    XMarkIcon, 
    PencilSquareIcon, 
    XCircleIcon, // Icono para cancelar
    CheckCircleIcon, 
    EyeIcon 
} from "@heroicons/react/24/solid";

const AlquileresList = () => {
    const [alquileres, setAlquileres] = useState([]);
    const [clientes, setClientes] = useState([]);
    const [vehiculos, setVehiculos] = useState([]);
    const [empleados, setEmpleados] = useState([]);
    
    const [isLoading, setIsLoading] = useState(true);
    const [filtroCliente, setFiltroCliente] = useState("");

    // Modales
    const [formVisible, setFormVisible] = useState(false);
    const [editVisible, setEditVisible] = useState(false);
    
    const [formData, setFormData] = useState({
        id: null,
        clienteId: '',
        vehiculoId: '',
        empleadoId: '',
        fechaInicio: '', 
        fechaFin: ''
    });

    const loadData = async () => {
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
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const formatFechaInput = (fechaStr) => {
        if (!fechaStr) return '';
        return fechaStr.replace(' ', 'T');
    };

    // --- ACTIONS ---

    // 1. CANCELAR (Lógica Transaccional)
    const handleCancel = async (id) => {
        const result = await Swal.fire({
            title: '¿Cancelar Alquiler?',
            text: "El alquiler pasará a estado 'Cancelado' y el vehículo quedará disponible. Esta acción es irreversible.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            confirmButtonText: 'Sí, Cancelar',
            cancelButtonText: 'No'
        });

        if (result.isConfirmed) {
            try {
                await cancelarAlquiler(id);
                Swal.fire('Cancelado', 'El alquiler ha sido cancelado.', 'success');
                loadData();
            } catch (error) {
                Swal.fire('Error', error.response?.data?.error || 'No se pudo cancelar.', 'error');
            }
        }
    };

    // 2. FINALIZAR (Lógica Transaccional)
    const handleFinalize = async (id) => {
        const { value: km } = await Swal.fire({
            title: 'Finalizar Alquiler',
            text: 'Ingrese el kilometraje de devolución:',
            input: 'number',
            inputLabel: 'Kilometraje Final',
            inputPlaceholder: 'Ej: 55000',
            showCancelButton: true,
            confirmButtonColor: '#10b981',
            confirmButtonText: 'Finalizar y Cobrar',
            inputValidator: (value) => {
                if (!value) return '¡El kilometraje es obligatorio!';
            }
        });

        if (km) {
            try {
                await finalizarAlquiler(id, km);
                Swal.fire('Finalizado', 'Alquiler cerrado correctamente.', 'success');
                loadData();
            } catch (error) {
                Swal.fire('Error', error.response?.data?.error || 'Error al finalizar.', 'error');
            }
        }
    };

    // 3. EDITAR
    const handleEditClick = (alq) => {
        setFormData({
            id: alq.id,
            clienteId: alq.cliente_id,
            vehiculoId: alq.vehiculo_id,
            empleadoId: alq.empleado_id,
            fechaInicio: formatFechaInput(alq.fecha_inicio),
            fechaFin: formatFechaInput(alq.fecha_fin)
        });
        setEditVisible(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (new Date(formData.fechaInicio) >= new Date(formData.fechaFin)) {
            Swal.fire('Error', 'La fecha de fin debe ser posterior al inicio.', 'warning');
            return;
        }

        try {
            if (editVisible) {
                await updateAlquiler(formData.id, formData);
                Swal.fire('Actualizado', 'Datos modificados.', 'success');
                setEditVisible(false);
            } else {
                await crearAlquiler(formData);
                Swal.fire('Registrado', 'Nuevo alquiler creado.', 'success');
                setFormVisible(false);
            }
            setFormData({ id: null, clienteId: '', vehiculoId: '', empleadoId: '', fechaInicio: '', fechaFin: '' });
            loadData(); 
        } catch (error) {
            Swal.fire('Error', error.response?.data?.error || 'Error en la operación.', 'error');
        }
    };

    const handleView = (alq) => {
        Swal.fire({
            title: '<strong>Detalle del Alquiler</strong>',
            html: `
                <div class="text-left text-sm">
                    <p><b>ID:</b> #${alq.id}</p>
                    <p><b>Vehículo:</b> ${alq.vehiculo}</p>
                    <p><b>Cliente:</b> ${alq.cliente}</p>
                    <p><b>Empleado:</b> ${alq.empleado}</p>
                    <hr class="my-2">
                    <p><b>Inicio:</b> ${alq.fecha_inicio}</p>
                    <p><b>Fin:</b> ${alq.fecha_fin}</p>
                    <p class="mt-2 text-lg"><b>Estado:</b> <span class="font-bold">${alq.estado}</span></p>
                    <p class="text-xl text-green-600"><b>Total:</b> $${alq.costo_total}</p>
                </div>
            `,
            confirmButtonText: 'Cerrar'
        });
    };

    const getEstadoStyle = (estado) => {
        // Normalizamos mayúsculas/minúsculas por las dudas
        const est = estado.toUpperCase();
        if (est.includes('CURSO')) return 'bg-green-100 text-green-800 border border-green-200';
        if (est.includes('FINALIZADO')) return 'bg-blue-100 text-blue-800 border border-blue-200';
        if (est.includes('CANCELADO')) return 'bg-red-100 text-red-800 border border-red-200';
        if (est.includes('RESERVADO')) return 'bg-yellow-100 text-yellow-800 border border-yellow-200';
        return 'bg-gray-100 text-gray-800';
    };

    // Filtrado
    const alquileresFiltrados = alquileres.filter((alquiler) => {
        if (!filtroCliente) return true;
        return alquiler.cliente_id === parseInt(filtroCliente);
    });

    if (isLoading) return <div className="text-center p-10 font-medium text-gray-500">Cargando transacciones...</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold text-gray-800">Gestión de Alquileres</h2>
                <button
                    onClick={() => {
                        setFormData({ id: null, clienteId: '', vehiculoId: '', empleadoId: '', fechaInicio: '', fechaFin: '' });
                        setFormVisible(true);
                    }}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-xl shadow-lg transition-all transform hover:scale-105"
                >
                    + Nuevo Alquiler
                </button>
            </div>

            {/* FILTRO */}
            <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex items-center gap-4">
                <div className="flex items-center text-gray-500 font-medium">
                    <FunnelIcon className="h-5 w-5 mr-2" />
                    Filtrar por Cliente:
                </div>
                <select
                    value={filtroCliente}
                    onChange={(e) => setFiltroCliente(e.target.value)}
                    className="border border-gray-300 rounded-lg p-2 text-sm w-64 focus:ring-2 focus:ring-indigo-500"
                >
                    <option value="">Todos</option>
                    {clientes.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                </select>
                {filtroCliente && (
                    <button onClick={() => setFiltroCliente("")} className="text-red-500 hover:text-red-700 font-medium text-sm flex items-center">
                        <XMarkIcon className="h-4 w-4 mr-1" /> Limpiar
                    </button>
                )}
            </div>

            {/* TABLA */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                            <tr>
                                <th className="px-6 py-4 text-left">ID</th>
                                <th className="px-6 py-4 text-left">Vehículo</th>
                                <th className="px-6 py-4 text-left">Cliente</th>
                                <th className="px-6 py-4 text-left">Periodo</th>
                                <th className="px-6 py-4 text-left">Estado</th>
                                <th className="px-6 py-4 text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200 text-sm">
                            {alquileresFiltrados.length > 0 ? (
                                alquileresFiltrados.map((a) => {
                                    const estadoUpper = a.estado.toUpperCase();
                                    const esActivo = estadoUpper.includes('CURSO') || estadoUpper.includes('RESERVADO');
                                    const esEnCurso = estadoUpper.includes('CURSO');

                                    return (
                                        <tr key={a.id} className="hover:bg-gray-50 transition-colors">
                                            <td className="px-6 py-4 text-gray-500">#{a.id}</td>
                                            <td className="px-6 py-4 font-medium text-gray-900">{a.vehiculo}</td>
                                            <td className="px-6 py-4 text-gray-600">{a.cliente}</td>
                                            <td className="px-6 py-4 text-gray-500">
                                                <div className="flex flex-col">
                                                    <span>In: {a.fecha_inicio}</span>
                                                    <span>Out: {a.fecha_fin}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getEstadoStyle(a.estado)}`}>
                                                    {a.estado}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-right whitespace-nowrap">
                                                <div className="flex justify-end gap-3">
                                                    
                                                    {/* VER DETALLE (Siempre visible) */}
                                                    <button onClick={() => handleView(a)} className="text-gray-400 hover:text-indigo-600" title="Ver Detalle">
                                                        <EyeIcon className="h-5 w-5" />
                                                    </button>

                                                    {/* MODIFICAR (Solo si es activo) */}
                                                    {esActivo && (
                                                        <button onClick={() => handleEditClick(a)} className="text-blue-400 hover:text-blue-600" title="Editar datos">
                                                            <PencilSquareIcon className="h-5 w-5" />
                                                        </button>
                                                    )}

                                                    {/* FINALIZAR (Solo si está En Curso) */}
                                                    {esEnCurso && (
                                                        <button onClick={() => handleFinalize(a.id)} className="text-green-500 hover:text-green-700" title="Finalizar Alquiler">
                                                            <CheckCircleIcon className="h-6 w-6" />
                                                        </button>
                                                    )}

                                                    {/* CANCELAR (Solo si es activo) */}
                                                    {esActivo && (
                                                        <button onClick={() => handleCancel(a.id)} className="text-red-400 hover:text-red-600" title="Cancelar Alquiler">
                                                            <XCircleIcon className="h-6 w-6" />
                                                        </button>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    );
                                })
                            ) : (
                                <tr>
                                    <td colSpan="6" className="px-6 py-10 text-center text-gray-500">
                                        No se encontraron alquileres.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* --- MODAL FORMULARIO (Crear/Editar) --- */}
            {(formVisible || editVisible) && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 backdrop-blur-sm">
                    <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-2xl transform transition-all scale-100">
                        <h3 className="text-2xl font-bold mb-6 text-gray-800 border-b pb-3">
                            {editVisible ? 'Modificar Alquiler' : 'Nuevo Alquiler'}
                        </h3>
                        <form onSubmit={handleSubmit} className="space-y-5">
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-1">Cliente</label>
                                    <select name="clienteId" value={formData.clienteId} onChange={handleInputChange} required className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 p-2 border">
                                        <option value="">Seleccione...</option>
                                        {clientes.map(c => <option key={c.id} value={c.id}>{c.nombre} ({c.dni})</option>)}
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-1">Vehículo</label>
                                    <select name="vehiculoId" value={formData.vehiculoId} onChange={handleInputChange} required className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 p-2 border">
                                        <option value="">Seleccione...</option>
                                        {vehiculos
                                            .filter(v => v.estado === 'Disponible' || v.estado === 'DISPONIBLE' || v.id === formData.vehiculoId)
                                            .map(v => (
                                                <option key={v.id} value={v.id}>{v.patente} - {v.modelo}</option>
                                            ))}
                                    </select>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-1">Fecha Inicio</label>
                                    <input type="datetime-local" name="fechaInicio" value={formData.fechaInicio} onChange={handleInputChange} required className="w-full border-gray-300 rounded-lg shadow-sm p-2 border" />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-1">Fecha Fin (Estimada)</label>
                                    <input type="datetime-local" name="fechaFin" value={formData.fechaFin} onChange={handleInputChange} required className="w-full border-gray-300 rounded-lg shadow-sm p-2 border" />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Empleado Responsable</label>
                                <select name="empleadoId" value={formData.empleadoId} onChange={handleInputChange} required className="w-full border-gray-300 rounded-lg shadow-sm p-2 border">
                                    <option value="">Seleccione...</option>
                                    {empleados.map(e => <option key={e.id} value={e.id}>{e.nombre}</option>)}
                                </select>
                            </div>

                            <div className="flex justify-end gap-3 pt-4">
                                <button type="button" onClick={() => { setFormVisible(false); setEditVisible(false); }} className="px-5 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-medium">
                                    Cancelar
                                </button>
                                <button type="submit" className="px-5 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium shadow-md">
                                    {editVisible ? 'Guardar Cambios' : 'Confirmar Alquiler'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AlquileresList;