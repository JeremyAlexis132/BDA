/**
 * Frontend JavaScript - Sistema de Gestión de Empleados
 * Proyecto Final - Base de Datos Avanzadas (UNAM)
 */

const API_URL = '';  // Mismo origen (Flask sirve el frontend)

// Estado global
let authToken = null;
let currentUser = null;
let empleadosData = [];
let departamentosData = [];

// ============================
// AUTENTICACIÓN
// ============================

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-user').value;
    const password = document.getElementById('login-pass').value;
    const alertEl = document.getElementById('login-alert');

    try {
        const res = await fetch(`${API_URL}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            alertEl.textContent = data.error || 'Error de autenticación';
            alertEl.classList.add('show');
            return;
        }

        authToken = data.token;
        currentUser = data.user;
        alertEl.classList.remove('show');

        // Mostrar app
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('app').style.display = 'block';
        document.getElementById('nav-username').textContent = currentUser.username;
        document.getElementById('nav-rol').textContent = currentUser.rol;

        // Mostrar/ocultar botones según rol
        if (currentUser.rol === 'admin') {
            document.getElementById('btn-add-emp').style.display = 'inline-flex';
            document.getElementById('btn-add-dept').style.display = 'inline-flex';
            document.getElementById('th-acciones').style.display = '';
        }

        // Cargar datos
        loadDashboard();
        loadEmpleados();
        loadDepartamentos();
        loadAuditoria();

    } catch (err) {
        alertEl.textContent = 'Error de conexión con el servidor';
        alertEl.classList.add('show');
    }
});

function logout() {
    authToken = null;
    currentUser = null;
    document.getElementById('app').style.display = 'none';
    document.getElementById('login-screen').style.display = 'flex';
    document.getElementById('login-user').value = '';
    document.getElementById('login-pass').value = '';
}

// ============================
// API HELPERS
// ============================

async function apiFetch(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    const res = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.error || `Error ${res.status}`);
    }

    return data;
}

function showAlert(message, type = 'success') {
    const alert = document.getElementById('global-alert');
    alert.className = `alert alert-${type} show`;
    alert.textContent = message;
    setTimeout(() => alert.classList.remove('show'), 4000);
}

// ============================
// TABS
// ============================

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

    document.getElementById(`tab-${tabName}`).classList.add('active');
    event.target.classList.add('active');
}

// ============================
// DASHBOARD
// ============================

async function loadDashboard() {
    try {
        const data = await apiFetch('/api/estadisticas');
        const s = data.estadisticas;

        document.getElementById('stat-activos').textContent = s.empleados_activos?.toLocaleString() || '0';
        document.getElementById('stat-inactivos').textContent = s.empleados_inactivos?.toLocaleString() || '0';
        document.getElementById('stat-departamentos').textContent = s.departamentos || '0';
        document.getElementById('stat-salario').textContent = s.salario_promedio
            ? `$${Number(s.salario_promedio).toLocaleString('es-MX', {minimumFractionDigits: 2})}`
            : '$0';
        document.getElementById('stat-auditorias').textContent = s.total_auditorias?.toLocaleString() || '0';

        // Top departamentos
        const tbody = document.getElementById('top-dept-body');
        if (s.top_departamentos && s.top_departamentos.length > 0) {
            tbody.innerHTML = s.top_departamentos.map(d => `
                <tr>
                    <td>${d.nombre}</td>
                    <td><strong>${d.total}</strong></td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="2">Sin datos</td></tr>';
        }
    } catch (err) {
        console.error('Error cargando dashboard:', err);
    }
}

// ============================
// EMPLEADOS
// ============================

async function loadEmpleados() {
    try {
        const data = await apiFetch('/api/empleados');
        empleadosData = data.empleados;
        renderEmpleados(empleadosData);
    } catch (err) {
        console.error('Error cargando empleados:', err);
        document.getElementById('empleados-body').innerHTML =
            `<tr><td colspan="8" style="padding:20px; color:red;">Error: ${err.message}</td></tr>`;
    }
}

function renderEmpleados(empleados) {
    const tbody = document.getElementById('empleados-body');
    const isAdmin = currentUser?.rol === 'admin';

    if (empleados.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="padding:20px;">No se encontraron empleados</td></tr>';
        return;
    }

    tbody.innerHTML = empleados.map(e => `
        <tr>
            <td>${e.id_empleado}</td>
            <td><strong>${e.nombre} ${e.apellido}</strong></td>
            <td>${e.email || '-'}</td>
            <td>${e.departamento}</td>
            <td>$${Number(e.salario).toLocaleString('es-MX', {minimumFractionDigits: 2})}</td>
            <td>${e.fecha_ingreso}</td>
            <td>
                <span class="badge ${e.activo === 'S' ? 'badge-success' : 'badge-danger'}">
                    ${e.activo === 'S' ? 'Activo' : 'Inactivo'}
                </span>
            </td>
            ${isAdmin ? `
            <td>
                <button class="btn btn-warning btn-sm" onclick="editEmpleado(${e.id_empleado})">✏️</button>
                <button class="btn btn-danger btn-sm" onclick="deleteEmpleado(${e.id_empleado}, '${e.nombre} ${e.apellido}')">🗑️</button>
            </td>
            ` : ''}
        </tr>
    `).join('');
}

function filterEmpleados() {
    const term = document.getElementById('search-empleados').value.toLowerCase();
    const filtered = empleadosData.filter(e =>
        e.nombre.toLowerCase().includes(term) ||
        e.apellido.toLowerCase().includes(term) ||
        (e.email && e.email.toLowerCase().includes(term)) ||
        e.departamento.toLowerCase().includes(term)
    );
    renderEmpleados(filtered);
}

function openEmpleadoModal(emp = null) {
    document.getElementById('modal-emp-title').textContent = emp ? 'Editar Empleado' : 'Agregar Empleado';
    document.getElementById('modal-emp-alert').classList.remove('show');

    // Cargar departamentos en select
    const select = document.getElementById('emp-departamento');
    select.innerHTML = '<option value="">Seleccionar...</option>' +
        departamentosData.map(d =>
            `<option value="${d.id_departamento}">${d.nombre}</option>`
        ).join('');

    if (emp) {
        document.getElementById('emp-id').value = emp.id_empleado;
        document.getElementById('emp-nombre').value = emp.nombre;
        document.getElementById('emp-apellido').value = emp.apellido;
        document.getElementById('emp-email').value = emp.email || '';
        document.getElementById('emp-fecha').value = emp.fecha_ingreso;
        document.getElementById('emp-salario').value = emp.salario;
        document.getElementById('emp-departamento').value = emp.id_departamento;
        document.getElementById('emp-nivel').value = emp.nivel_seguridad || 'INTERNO';
        document.getElementById('emp-activo').value = emp.activo || 'S';
    } else {
        document.getElementById('emp-id').value = '';
        document.getElementById('form-empleado').reset();
    }

    document.getElementById('modal-empleado').classList.add('show');
}

async function editEmpleado(id) {
    try {
        const data = await apiFetch(`/api/empleados/${id}`);
        openEmpleadoModal(data.empleado);
    } catch (err) {
        showAlert(err.message, 'danger');
    }
}

async function saveEmpleado() {
    const id = document.getElementById('emp-id').value;
    const alertEl = document.getElementById('modal-emp-alert');

    const body = {
        nombre: document.getElementById('emp-nombre').value,
        apellido: document.getElementById('emp-apellido').value,
        email: document.getElementById('emp-email').value,
        fecha_ingreso: document.getElementById('emp-fecha').value,
        salario: document.getElementById('emp-salario').value,
        id_departamento: document.getElementById('emp-departamento').value,
        nivel_seguridad: document.getElementById('emp-nivel').value,
        activo: document.getElementById('emp-activo').value
    };

    // Validación básica
    if (!body.nombre || !body.apellido || !body.email || !body.fecha_ingreso ||
        !body.salario || !body.id_departamento) {
        alertEl.textContent = 'Complete todos los campos requeridos';
        alertEl.classList.add('show');
        return;
    }

    try {
        if (id) {
            await apiFetch(`/api/empleados/${id}`, {
                method: 'PUT',
                body: JSON.stringify(body)
            });
            showAlert('Empleado actualizado exitosamente');
        } else {
            await apiFetch('/api/empleados', {
                method: 'POST',
                body: JSON.stringify(body)
            });
            showAlert('Empleado creado exitosamente');
        }

        closeModal('modal-empleado');
        loadEmpleados();
        loadDashboard();
    } catch (err) {
        alertEl.textContent = err.message;
        alertEl.classList.add('show');
    }
}

async function deleteEmpleado(id, nombre) {
    if (!confirm(`¿Desactivar al empleado "${nombre}"?\nSe realizará un borrado lógico.`)) return;

    try {
        await apiFetch(`/api/empleados/${id}`, { method: 'DELETE' });
        showAlert(`Empleado "${nombre}" desactivado exitosamente`);
        loadEmpleados();
        loadDashboard();
        loadAuditoria();
    } catch (err) {
        showAlert(err.message, 'danger');
    }
}

// ============================
// DEPARTAMENTOS
// ============================

async function loadDepartamentos() {
    try {
        const data = await apiFetch('/api/departamentos');
        departamentosData = data.departamentos;
        renderDepartamentos(departamentosData);
    } catch (err) {
        console.error('Error cargando departamentos:', err);
    }
}

function renderDepartamentos(departamentos) {
    const tbody = document.getElementById('departamentos-body');
    tbody.innerHTML = departamentos.map(d => `
        <tr>
            <td>${d.id_departamento}</td>
            <td><strong>${d.nombre}</strong></td>
            <td>${d.ubicacion || '-'}</td>
            <td>
                <span class="badge ${d.estado === 'A' ? 'badge-success' : 'badge-danger'}">
                    ${d.estado === 'A' ? 'Activo' : 'Inactivo'}
                </span>
            </td>
        </tr>
    `).join('');
}

function openDeptModal() {
    document.getElementById('modal-dept-alert').classList.remove('show');
    document.getElementById('dept-nombre').value = '';
    document.getElementById('dept-ubicacion').value = '';
    document.getElementById('modal-departamento').classList.add('show');
}

async function saveDepartamento() {
    const alertEl = document.getElementById('modal-dept-alert');
    const nombre = document.getElementById('dept-nombre').value;

    if (!nombre) {
        alertEl.textContent = 'El nombre es requerido';
        alertEl.classList.add('show');
        return;
    }

    try {
        await apiFetch('/api/departamentos', {
            method: 'POST',
            body: JSON.stringify({
                nombre: nombre,
                ubicacion: document.getElementById('dept-ubicacion').value
            })
        });

        closeModal('modal-departamento');
        showAlert('Departamento creado exitosamente');
        loadDepartamentos();
        loadDashboard();
    } catch (err) {
        alertEl.textContent = err.message;
        alertEl.classList.add('show');
    }
}

// ============================
// AUDITORÍA
// ============================

async function loadAuditoria() {
    try {
        const data = await apiFetch('/api/auditoria');
        const tbody = document.getElementById('auditoria-body');

        if (data.auditoria.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="padding:20px;">Sin registros de auditoría</td></tr>';
            return;
        }

        tbody.innerHTML = data.auditoria.map(a => {
            let badgeClass = 'badge-info';
            if (a.accion === 'INSERT') badgeClass = 'badge-success';
            if (a.accion === 'DELETE') badgeClass = 'badge-danger';
            if (a.accion === 'UPDATE') badgeClass = 'badge-warning';

            return `
                <tr>
                    <td>${a.audit_id}</td>
                    <td>${a.id_empleado || '-'}</td>
                    <td><span class="badge ${badgeClass}">${a.accion}</span></td>
                    <td>${a.usuario_bd || '-'}</td>
                    <td>${a.fecha_evento}</td>
                    <td>${a.salario_ant ? '$' + Number(a.salario_ant).toLocaleString('es-MX') : '-'}</td>
                    <td>${a.salario_nvo ? '$' + Number(a.salario_nvo).toLocaleString('es-MX') : '-'}</td>
                </tr>
            `;
        }).join('');
    } catch (err) {
        console.error('Error cargando auditoría:', err);
    }
}

// ============================
// MODALES
// ============================

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// Cerrar modal con clic fuera
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.classList.remove('show');
        }
    });
});

// Cerrar modal con Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.show').forEach(m => m.classList.remove('show'));
    }
});
