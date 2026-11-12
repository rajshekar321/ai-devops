// AI-DevOps Control Center Frontend Logic

const API_BASE = '/api/v1';

async function fetchHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();

        const apiEl = document.getElementById('api-status-val');
        const dbEl = document.getElementById('db-status-val');
        const badgeEl = document.getElementById('system-badge');
        const envEl = document.getElementById('env-val');

        if (res.ok && data.status === 'healthy') {
            apiEl.textContent = 'ONLINE';
            apiEl.style.color = 'var(--accent-green)';
            dbEl.textContent = data.database_connected ? 'CONNECTED' : 'DISCONNECTED';
            dbEl.style.color = data.database_connected ? 'var(--accent-green)' : 'var(--accent-red)';
            badgeEl.className = 'badge badge-success';
            badgeEl.innerHTML = '<span class="pulse-dot"></span> System Operational';
        } else {
            apiEl.textContent = 'DEGRADED';
            apiEl.style.color = 'var(--accent-yellow)';
            dbEl.textContent = data.database_connected ? 'CONNECTED' : 'OFFLINE';
            dbEl.style.color = data.database_connected ? 'var(--accent-green)' : 'var(--accent-red)';
            badgeEl.className = 'badge badge-warning';
            badgeEl.innerHTML = '<span class="pulse-dot"></span> Degraded';
        }
        if (data.environment) {
            envEl.textContent = data.environment.toUpperCase();
        }
    } catch (err) {
        console.error('Health check failed:', err);
        const apiEl = document.getElementById('api-status-val');
        const badgeEl = document.getElementById('system-badge');
        apiEl.textContent = 'UNREACHABLE';
        apiEl.style.color = 'var(--accent-red)';
        badgeEl.className = 'badge badge-danger';
        badgeEl.innerHTML = '<span class="pulse-dot"></span> Service Offline';
    }
}

async function loadTasks() {
    const tbody = document.getElementById('tasks-tbody');
    try {
        const res = await fetch(`${API_BASE}/tasks`);
        const tasks = await res.json();

        if (!tasks || tasks.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No tasks recorded yet. Create one above!</td></tr>';
            return;
        }

        tbody.innerHTML = tasks.map(t => `
            <tr>
                <td>#${t.id}</td>
                <td>
                    <strong>${escapeHtml(t.title)}</strong>
                    ${t.description ? `<br><small style="color:var(--text-secondary)">${escapeHtml(t.description)}</small>` : ''}
                </td>
                <td><span class="badge ${getPriorityClass(t.priority)}">${t.priority}</span></td>
                <td><span class="badge ${getStatusClass(t.status)}">${t.status}</span></td>
                <td>
                    ${t.status !== 'completed' ? `<button onclick="updateTaskStatus(${t.id}, 'completed')" class="btn btn-sm btn-outline">Complete</button>` : ''}
                    <button onclick="deleteTask(${t.id})" class="btn btn-sm btn-danger">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center" style="color:var(--accent-red)">Failed to load tasks.</td></tr>';
    }
}

async function createTask(e) {
    e.preventDefault();
    const title = document.getElementById('task-title').value.trim();
    const description = document.getElementById('task-desc').value.trim();
    const priority = document.getElementById('task-priority').value;

    if (!title) return;

    try {
        const res = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description, priority })
        });

        if (res.ok) {
            document.getElementById('task-title').value = '';
            document.getElementById('task-desc').value = '';
            await loadTasks();
        } else {
            alert('Failed to create task');
        }
    } catch (err) {
        console.error('Error creating task:', err);
    }
}

async function updateTaskStatus(id, newStatus) {
    try {
        const res = await fetch(`${API_BASE}/tasks/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        if (res.ok) {
            await loadTasks();
        }
    } catch (err) {
        console.error('Failed to update task:', err);
    }
}

async function deleteTask(id) {
    if (!confirm(`Delete task #${id}?`)) return;
    try {
        const res = await fetch(`${API_BASE}/tasks/${id}`, {
            method: 'DELETE'
        });
        if (res.ok) {
            await loadTasks();
        }
    } catch (err) {
        console.error('Failed to delete task:', err);
    }
}

function getPriorityClass(p) {
    switch (p) {
        case 'critical': return 'badge-danger';
        case 'high': return 'badge-warning';
        case 'low': return 'badge-info';
        default: return 'badge-info';
    }
}

function getStatusClass(s) {
    switch (s) {
        case 'completed': return 'badge-success';
        case 'in_progress': return 'badge-info';
        case 'failed': return 'badge-danger';
        default: return 'badge-warning';
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

document.addEventListener('DOMContentLoaded', () => {
    fetchHealth();
    loadTasks();
    document.getElementById('task-form').addEventListener('submit', createTask);
    document.getElementById('refresh-tasks-btn').addEventListener('click', loadTasks);
    setInterval(fetchHealth, 15000);
});
