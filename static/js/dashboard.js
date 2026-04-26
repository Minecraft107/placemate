const API_BASE = 'http://localhost:5000/api';
const token = localStorage.getItem('access_token');

// Always check auth first
if (!token) {
    window.location.href = '/login';
}

const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

// Upload resume
document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = document.getElementById('resume-file').files[0];
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE}/resume/upload`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },  // no Content-Type for FormData
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayATSResult(data);
        } else {
            showError(data.error);
        }
    } catch (err) {
        showError('Network error. Is the server running?');
    } finally {
        showLoading(false);
    }
});

function displayATSResult(data) {
    // Update ATS score badge
    document.getElementById('ats-score').textContent = data.ats_score + '%';
    
    // Show matched keywords
    const matchedDiv = document.getElementById('keywords-matched');
    matchedDiv.innerHTML = data.keywords_matched
        .map(kw => `<span class="badge bg-success me-1">${kw}</span>`)
        .join('');
    
    // Show missing keywords
    const missingDiv = document.getElementById('keywords-missing');
    missingDiv.innerHTML = data.missing_keywords
        .map(kw => `<span class="badge bg-danger me-1">${kw}</span>`)
        .join('');
    
    // Show suggestions
    const sugDiv = document.getElementById('suggestions');
    sugDiv.innerHTML = data.suggestions
        .map(s => `<li class="list-group-item">${s}</li>`)
        .join('');
}

// Prediction form
document.getElementById('predict-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const payload = {
        cgpa: parseFloat(document.getElementById('cgpa').value),
        backlogs: parseInt(document.getElementById('backlogs').value),
        internship_done: document.getElementById('internship').checked ? 1 : 0,
        projects_count: parseInt(document.getElementById('projects').value),
        skills_count: parseInt(document.getElementById('skills_count').value),
        ats_score: parseFloat(document.getElementById('ats_score').value),
        communication_score: parseInt(document.getElementById('comm_score').value),
        model: document.getElementById('model-select').value
    };
    
    const response = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
    });
    
    const result = await response.json();
    displayPrediction(result);
});

function displayPrediction(result) {
    const outcomeEl = document.getElementById('prediction-outcome');
    const badge = result.outcome === 'Placed' ? 'bg-success' : 'bg-danger';
    outcomeEl.innerHTML = `
        <span class="badge ${badge} fs-4 p-3">${result.outcome}</span>
        <p class="mt-2">Confidence: <strong>${result.confidence}%</strong></p>
        <p>Placement probability: <strong>${result.placed_probability}%</strong></p>
        <small class="text-muted">Model: ${result.model_used}</small>
    `;
}