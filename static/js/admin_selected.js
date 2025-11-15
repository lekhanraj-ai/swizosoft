// Fetch selected candidates and render cards
document.addEventListener('DOMContentLoaded', function() {
    loadSelected();
});

function loadSelected() {
    const grid = document.getElementById('selectedGrid');
    const countElem = document.getElementById('selected-count');
    
    fetch('/admin/api/get-selected', {
        method: 'GET',
        credentials: 'include',  // Include session cookies
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(r => {
            console.log('Response status:', r.status);
            return r.json();
        })
        .then(resp => {
            console.log('Response data:', resp);
            if (resp.success) {
                renderSelected(grid, countElem, resp.data || []);
            } else {
                grid.innerHTML = `<div class="empty-card"><div class="empty-card-icon">⚠️</div><p>Error: ${resp.error || 'Unknown'}</p></div>`;
                countElem.textContent = '0';
            }
        })
        .catch(err => {
            console.error('Fetch error:', err);
            grid.innerHTML = `<div class="empty-card"><div class="empty-card-icon">⚠️</div><p>Could not fetch selected candidates: ${err.message}</p></div>`;
            countElem.textContent = '0';
        });
}

function renderSelected(container, countElem, rows) {
    container.innerHTML = '';
    if (!rows || rows.length === 0) {
        container.innerHTML = `
            <div class="empty-card">
                <div class="empty-card-icon">📭</div>
                <p>No selected candidates yet</p>
            </div>
        `;
        countElem.textContent = '0';
        return;
    }

    countElem.textContent = rows.length;

    // Create table
    const table = document.createElement('table');
    table.className = 'applicants-table';
    
    // Table header
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Name</th>
            <th>USN</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Branch</th>
            <th>View Resume</th>
            <th>View ID Proof</th>
            <th>View Project</th>
        </tr>
    `;
    table.appendChild(thead);
    
    // Table body
    const tbody = document.createElement('tbody');
    
    rows.forEach(r => {
        const tr = document.createElement('tr');
        
        // Extract candidate details with fallback
        function getField(keys) {
            if (!r) return null;
            for (const k of keys) {
                if (r[k] !== undefined && r[k] !== null && r[k] !== '') return r[k];
            }
            return null;
        }

        const name = getField(['name', 'full_name', 'applicant_name', 'student_name']) || 'N/A';
        const usn = getField(['usn', 'roll', 'rollno', 'roll_no']) || 'N/A';
        const email = getField(['email', 'applicant_email', 'email_address']) || 'N/A';
        const phone = getField(['phone', 'mobile', 'contact', 'phone_number']) || 'N/A';
        const branch = getField(['branch', 'department', 'stream']) || 'N/A';
        const appId = r.application_id || r.original_id || r.id;

        // Build file view buttons
        const resumeBtn = appId ? `<button class="table-action-btn table-view-btn" onclick="viewFile(${appId}, 'resume', 'paid')">View Resume</button>` : '—';
        const idProofBtn = appId ? `<button class="table-action-btn table-view-btn" onclick="viewFile(${appId}, 'id_proof', 'paid')">View ID Proof</button>` : '—';
        const projectBtn = appId ? `<button class="table-action-btn table-view-btn" onclick="viewFile(${appId}, 'project', 'paid')">View Project</button>` : '—';

        tr.innerHTML = `
            <td class="table-name">${name}</td>
            <td class="table-usn">${usn}</td>
            <td>${email}</td>
            <td>${phone}</td>
            <td>${branch}</td>
            <td>${resumeBtn}</td>
            <td>${idProofBtn}</td>
            <td>${projectBtn}</td>
        `;
        
        tbody.appendChild(tr);
    });
    
    table.appendChild(tbody);
    container.appendChild(table);
}
