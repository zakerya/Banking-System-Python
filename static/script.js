// Tab switching functionality
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs and content
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding content
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});

// Add event listeners to buttons
document.getElementById('createAccountBtn').addEventListener('click', createAccount);
document.getElementById('depositBtn').addEventListener('click', depositMoney);
document.getElementById('withdrawBtn').addEventListener('click', withdrawMoney);
document.getElementById('balanceBtn').addEventListener('click', checkBalance);
document.getElementById('deleteBtn').addEventListener('click', deleteAccount);
document.getElementById('refreshBtn').addEventListener('click', loadAccounts);

// API call functions
async function apiCall(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        return { success: false, message: 'Network error: ' + error.message };
    }
}

// Create account function
async function createAccount() {
    const name = document.getElementById('name').value.trim();
    const pin = document.getElementById('pin').value.trim();
    const messageDiv = document.getElementById('createAccountMessage');
    
    if (!name) {
        showMessage(messageDiv, 'Please enter your name', 'error');
        return;
    }
    
    if (pin.length !== 4 || !/^\d+$/.test(pin)) {
        showMessage(messageDiv, 'PIN must be a 4-digit number', 'error');
        return;
    }
    
    const result = await apiCall('/api/create_account', { name, pin });
    
    if (result.success) {
        showMessage(messageDiv, result.message, 'success');
        document.getElementById('name').value = '';
        document.getElementById('pin').value = '';
    } else {
        showMessage(messageDiv, result.message, 'error');
    }
}

// Deposit money function
async function depositMoney() {
    const account = document.getElementById('depositAccount').value.trim();
    const pin = document.getElementById('depositPin').value.trim();
    const amount = document.getElementById('depositAmount').value.trim();
    const messageDiv = document.getElementById('depositMessage');
    
    if (!validateAccountInputs(account, pin, amount, messageDiv)) return;
    
    const result = await apiCall('/api/deposit', {
        account_number: parseInt(account),
        pin: parseInt(pin),
        amount: parseFloat(amount)
    });
    
    showMessage(messageDiv, result.message, result.success ? 'success' : 'error');
}

// Withdraw money function
async function withdrawMoney() {
    const account = document.getElementById('withdrawAccount').value.trim();
    const pin = document.getElementById('withdrawPin').value.trim();
    const amount = document.getElementById('withdrawAmount').value.trim();
    const messageDiv = document.getElementById('withdrawMessage');
    
    if (!validateAccountInputs(account, pin, amount, messageDiv)) return;
    
    const result = await apiCall('/api/withdraw', {
        account_number: parseInt(account),
        pin: parseInt(pin),
        amount: parseFloat(amount)
    });
    
    showMessage(messageDiv, result.message, result.success ? 'success' : 'error');
}

// Check balance function
async function checkBalance() {
    const account = document.getElementById('balanceAccount').value.trim();
    const pin = document.getElementById('balancePin').value.trim();
    const messageDiv = document.getElementById('balanceMessage');
    
    if (account.length !== 7 || !/^\d+$/.test(account)) {
        showMessage(messageDiv, 'Account number must be a 7-digit number', 'error');
        return;
    }
    
    if (pin.length !== 4 || !/^\d+$/.test(pin)) {
        showMessage(messageDiv, 'PIN must be a 4-digit number', 'error');
        return;
    }
    
    const result = await apiCall('/api/balance', {
        account_number: parseInt(account),
        pin: parseInt(pin)
    });
    
    if (result.success) {
        showMessage(messageDiv, 
            `Account Holder: ${result.account_name}<br>
            Account Number: ${result.account_number}<br>
            Current Balance: ${result.currency}${result.balance.toFixed(2)}`, 
            'success');
    } else {
        showMessage(messageDiv, result.message, 'error');
    }
}

// Delete account function
async function deleteAccount() {
    const account = document.getElementById('deleteAccount').value.trim();
    const pin = document.getElementById('deletePin').value.trim();
    const messageDiv = document.getElementById('deleteMessage');
    
    if (account.length !== 7 || !/^\d+$/.test(account)) {
        showMessage(messageDiv, 'Account number must be a 7-digit number', 'error');
        return;
    }
    
    if (pin.length !== 4 || !/^\d+$/.test(pin)) {
        showMessage(messageDiv, 'PIN must be a 4-digit number', 'error');
        return;
    }
    
    const result = await apiCall('/api/delete_account', {
        account_number: parseInt(account),
        pin: parseInt(pin)
    });
    
    showMessage(messageDiv, result.message, result.success ? 'success' : 'error');
}

// Load accounts function
async function loadAccounts() {
    try {
        const response = await fetch('/api/accounts');
        const result = await response.json();
        const accountsList = document.getElementById('accountsList');
        
        if (result.success && result.accounts.length > 0) {
            let html = '<table><tr><th>Account Number</th><th>Name</th><th>Balance</th></tr>';
            
            result.accounts.forEach(account => {
                html += `<tr>
                    <td>${account.account_number}</td>
                    <td>${account.name}</td>
                    <td>${account.currency}${account.balance.toFixed(2)}</td>
                </tr>`;
            });
            
            html += '</table>';
            accountsList.innerHTML = html;
        } else {
            accountsList.innerHTML = '<p>No accounts found</p>';
        }
    } catch (error) {
        document.getElementById('accountsList').innerHTML = 
            '<p class="error">Error loading accounts: ' + error.message + '</p>';
    }
}

// Helper functions
function validateAccountInputs(account, pin, amount, messageDiv) {
    if (account.length !== 7 || !/^\d+$/.test(account)) {
        showMessage(messageDiv, 'Account number must be a 7-digit number', 'error');
        return false;
    }
    
    if (pin.length !== 4 || !/^\d+$/.test(pin)) {
        showMessage(messageDiv, 'PIN must be a 4-digit number', 'error');
        return false;
    }
    
    if (!amount || parseFloat(amount) <= 0) {
        showMessage(messageDiv, 'Please enter a valid amount', 'error');
        return false;
    }
    
    return true;
}

function showMessage(element, message, type) {
    element.innerHTML = message;
    element.className = `message ${type}`;
}

// Load accounts when the page loads
window.onload = loadAccounts;