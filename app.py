from flask import Flask, request, jsonify, render_template
import random
import os

app = Flask(__name__)

class BankAccount:
    def __init__(self, account_number, pin, name, currency='$', balance=0.0):
        self.account_number = account_number
        self.pin = pin
        self.name = name
        self.currency = currency
        self.balance = balance
    
    def to_dict(self):
        return {
            'account_number': self.account_number,
            'pin': self.pin,
            'name': self.name,
            'currency': self.currency,
            'balance': self.balance
        }
    
    @staticmethod
    def from_dict(data):
        return BankAccount(
            data['account_number'],
            data['pin'],
            data['name'],
            data.get('currency', '$'),
            data.get('balance', 0.0)
        )

class BankSystem:
    FILE_NAME = "bank.dat"
    
    def __init__(self):
        self.accounts = []
        self.load_accounts()
    
    def load_accounts(self):
        self.accounts = []
        if not os.path.exists(self.FILE_NAME):
            return
        
        with open(self.FILE_NAME, 'r') as file:
            for line in file:
                try:
                    data = eval(line.strip())
                    account = BankAccount.from_dict(data)
                    self.accounts.append(account)
                except:
                    continue
    
    def save_accounts(self):
        with open(self.FILE_NAME, 'w') as file:
            for account in self.accounts:
                file.write(str(account.to_dict()) + '\n')
    
    def generate_account_number(self):
        while True:
            account_number = random.randint(1000000, 9999999)
            if not any(acc.account_number == account_number for acc in self.accounts):
                return account_number
    
    def create_account(self, pin, name):
        account_number = self.generate_account_number()
        new_account = BankAccount(account_number, pin, name)
        self.accounts.append(new_account)
        self.save_accounts()
        return new_account
    
    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None
    
    def verify_account(self, account_number, pin):
        account = self.find_account(account_number)
        if account and account.pin == pin:
            return account
        return None
    
    def deposit(self, account_number, pin, amount):
        account = self.verify_account(account_number, pin)
        if not account:
            return False, "Invalid account number or PIN"
        
        if amount <= 0:
            return False, "Invalid deposit amount"
        
        account.balance += amount
        self.save_accounts()
        return True, f"Deposit successful! New balance: {account.currency}{account.balance:.2f}"
    
    def withdraw(self, account_number, pin, amount):
        account = self.verify_account(account_number, pin)
        if not account:
            return False, "Invalid account number or PIN"
        
        if amount <= 0:
            return False, "Invalid withdrawal amount"
        
        if amount > account.balance:
            return False, "Insufficient funds"
        
        account.balance -= amount
        self.save_accounts()
        return True, f"Withdrawal successful! New balance: {account.currency}{account.balance:.2f}"
    
    def get_balance(self, account_number, pin):
        account = self.verify_account(account_number, pin)
        if not account:
            return False, "Invalid account number or PIN"
        return True, account.balance
    
    def delete_account(self, account_number, pin):
        account = self.verify_account(account_number, pin)
        if not account:
            return False, "Invalid account number or PIN"
        
        self.accounts.remove(account)
        self.save_accounts()
        return True, "Account deleted successfully"
    
    def get_all_accounts(self):
        return self.accounts

# Initialize the bank system
bank_system = BankSystem()

# API Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create_account', methods=['POST'])
def api_create_account():
    data = request.get_json()
    name = data.get('name')
    pin = data.get('pin')
    
    if not name or not pin:
        return jsonify({'success': False, 'message': 'Name and PIN are required'})
    
    if len(str(pin)) != 4 or not str(pin).isdigit():
        return jsonify({'success': False, 'message': 'PIN must be a 4-digit number'})
    
    new_account = bank_system.create_account(int(pin), name)
    return jsonify({
        'success': True, 
        'message': f'Account created successfully! Your account number is {new_account.account_number}',
        'account_number': new_account.account_number
    })

@app.route('/api/deposit', methods=['POST'])
def api_deposit():
    data = request.get_json()
    account_number = data.get('account_number')
    pin = data.get('pin')
    amount = data.get('amount')
    
    if not all([account_number, pin, amount]):
        return jsonify({'success': False, 'message': 'Account number, PIN, and amount are required'})
    
    try:
        account_number = int(account_number)
        pin = int(pin)
        amount = float(amount)
    except:
        return jsonify({'success': False, 'message': 'Invalid input format'})
    
    success, message = bank_system.deposit(account_number, pin, amount)
    return jsonify({'success': success, 'message': message})

@app.route('/api/withdraw', methods=['POST'])
def api_withdraw():
    data = request.get_json()
    account_number = data.get('account_number')
    pin = data.get('pin')
    amount = data.get('amount')
    
    if not all([account_number, pin, amount]):
        return jsonify({'success': False, 'message': 'Account number, PIN, and amount are required'})
    
    try:
        account_number = int(account_number)
        pin = int(pin)
        amount = float(amount)
    except:
        return jsonify({'success': False, 'message': 'Invalid input format'})
    
    success, message = bank_system.withdraw(account_number, pin, amount)
    return jsonify({'success': success, 'message': message})

@app.route('/api/balance', methods=['POST'])
def api_balance():
    data = request.get_json()
    account_number = data.get('account_number')
    pin = data.get('pin')
    
    if not account_number or not pin:
        return jsonify({'success': False, 'message': 'Account number and PIN are required'})
    
    try:
        account_number = int(account_number)
        pin = int(pin)
    except:
        return jsonify({'success': False, 'message': 'Invalid input format'})
    
    success, result = bank_system.get_balance(account_number, pin)
    if success:
        account = bank_system.find_account(account_number)
        return jsonify({
            'success': True, 
            'balance': result,
            'account_name': account.name,
            'account_number': account.account_number,
            'currency': account.currency
        })
    else:
        return jsonify({'success': False, 'message': result})

@app.route('/api/delete_account', methods=['POST'])
def api_delete_account():
    data = request.get_json()
    account_number = data.get('account_number')
    pin = data.get('pin')
    
    if not account_number or not pin:
        return jsonify({'success': False, 'message': 'Account number and PIN are required'})
    
    try:
        account_number = int(account_number)
        pin = int(pin)
    except:
        return jsonify({'success': False, 'message': 'Invalid input format'})
    
    success, message = bank_system.delete_account(account_number, pin)
    return jsonify({'success': success, 'message': message})

@app.route('/api/accounts', methods=['GET'])
def api_get_accounts():
    accounts = bank_system.get_all_accounts()
    accounts_data = [{
        'account_number': acc.account_number,
        'name': acc.name,
        'balance': acc.balance,
        'currency': acc.currency
    } for acc in accounts]
    
    return jsonify({'success': True, 'accounts': accounts_data})

if __name__ == '__main__':
    app.run(debug=True)