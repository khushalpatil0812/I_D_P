// ============================================
// AI-Based IDP System - Main JavaScript
// ============================================

// ===== Form Validation =====
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            showError(input, 'This field is required');
        } else {
            input.classList.remove('error');
            removeError(input);
        }
    });

    // Email validation
    const emailInputs = form.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        if (input.value && !validateEmail(input.value)) {
            isValid = false;
            input.classList.add('error');
            showError(input, 'Please enter a valid email address');
        }
    });

    return isValid;
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showError(input, message) {
    removeError(input);
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = '#ef4444';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
}

function removeError(input) {
    const errorDiv = input.parentNode.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// ===== Confirmation Dialogs =====
function confirmAction(message, callback) {
    if (confirm(message)) {
        if (callback) callback();
        return true;
    }
    return false;
}

function confirmGenerateIDP(employeeId, employeeName) {
    const message = `Are you sure you want to generate an IDP for ${employeeName}?\n\nThis will:\n- Analyze their current skills\n- Identify skill gaps\n- Generate personalized development recommendations using AI`;
    return confirmAction(message);
}

function confirmDelete(itemType, itemName) {
    const message = `Are you sure you want to delete this ${itemType}?\n\n"${itemName}"\n\nThis action cannot be undone.`;
    return confirmAction(message);
}

// ===== Progress Bar Updates =====
function updateProgressBar(progressBarId, value) {
    const progressBar = document.getElementById(progressBarId);
    if (progressBar) {
        progressBar.style.width = value + '%';
        progressBar.textContent = value + '%';
        
        // Change color based on completion
        if (value >= 80) {
            progressBar.style.background = 'linear-gradient(90deg, #10b981 0%, #059669 100%)';
        } else if (value >= 50) {
            progressBar.style.background = 'linear-gradient(90deg, #f59e0b 0%, #d97706 100%)';
        } else {
            progressBar.style.background = 'linear-gradient(90deg, #2563eb 0%, #3b82f6 100%)';
        }
    }
}

// ===== Dynamic Form Updates =====
function addSkillField() {
    const container = document.getElementById('skills-container');
    if (!container) return;

    const skillDiv = document.createElement('div');
    skillDiv.className = 'form-group skill-field';
    skillDiv.innerHTML = `
        <input type="text" class="form-control" name="skill[]" placeholder="Enter skill">
        <button type="button" class="btn btn-danger btn-sm" onclick="removeSkillField(this)">Remove</button>
    `;
    container.appendChild(skillDiv);
}

function removeSkillField(button) {
    button.parentElement.remove();
}

// ===== CSV File Validation =====
function validateCSVFile(input) {
    const file = input.files[0];
    if (!file) return false;

    const fileName = file.name;
    const fileExtension = fileName.split('.').pop().toLowerCase();

    if (fileExtension !== 'csv') {
        alert('Please upload a CSV file only.');
        input.value = '';
        return false;
    }

    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
        alert('File size must be less than 5MB.');
        input.value = '';
        return false;
    }

    // Show file name
    const fileNameDisplay = document.getElementById('file-name-display');
    if (fileNameDisplay) {
        fileNameDisplay.textContent = `Selected: ${fileName}`;
        fileNameDisplay.style.color = '#10b981';
    }

    return true;
}

// ===== Loading Spinner =====
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner"></div>';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// ===== Toast Notifications =====
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.style.maxWidth = '400px';
    toast.style.animation = 'slideIn 0.3s ease';

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===== Table Search/Filter =====
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;

    const filter = input.value.toUpperCase();
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;

        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell) {
                const textValue = cell.textContent || cell.innerText;
                if (textValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }

        rows[i].style.display = found ? '' : 'none';
    }
}

// ===== Progress Update Handler =====
function updateProgress(idpId) {
    const completionInput = document.getElementById(`completion-${idpId}`);
    const feedbackInput = document.getElementById(`feedback-${idpId}`);

    if (!completionInput) return false;

    const completion = parseInt(completionInput.value);

    if (isNaN(completion) || completion < 0 || completion > 100) {
        alert('Please enter a valid completion percentage (0-100)');
        return false;
    }

    if (confirm(`Update progress to ${completion}%?`)) {
        // Update progress bar visually
        updateProgressBar(`progress-bar-${idpId}`, completion);
        showToast('Progress updated successfully!', 'success');
        return true;
    }

    return false;
}

// ===== Auto-save Draft =====
let autoSaveTimer;
function enableAutoSave(formId, saveCallback) {
    const form = document.getElementById(formId);
    if (!form) return;

    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => {
                if (saveCallback) saveCallback();
                showToast('Draft saved', 'info');
            }, 2000);
        });
    });
}

// ===== Character Counter =====
function addCharacterCounter(textareaId, maxLength) {
    const textarea = document.getElementById(textareaId);
    if (!textarea) return;

    const counter = document.createElement('div');
    counter.className = 'char-counter text-muted';
    counter.style.fontSize = '0.875rem';
    counter.style.marginTop = '0.25rem';
    textarea.parentNode.appendChild(counter);

    function updateCounter() {
        const remaining = maxLength - textarea.value.length;
        counter.textContent = `${remaining} characters remaining`;
        counter.style.color = remaining < 50 ? '#ef4444' : '#64748b';
    }

    textarea.addEventListener('input', updateCounter);
    textarea.setAttribute('maxlength', maxLength);
    updateCounter();
}

// ===== Initialize on Page Load =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('IDP System JavaScript Loaded');

    // Add form submit validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this.id)) {
                e.preventDefault();
                showToast('Please fill in all required fields correctly', 'danger');
            }
        });
    });

    // Initialize progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const value = parseInt(bar.textContent) || 0;
        updateProgressBar(bar.id, value);
    });

    // Add active class to current nav link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// ===== Animation Keyframes (CSS-in-JS fallback) =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .error {
        border-color: #ef4444 !important;
    }
`;
document.head.appendChild(style);
