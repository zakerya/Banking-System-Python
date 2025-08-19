import sys
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QDialog, 
    QDialogButtonBox, QFormLayout, QGroupBox, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class BankAccount:
    def __init__(self, account_number, pin, name, currency='$', balance=0.0):
        self.account_number = account_number
        self.pin = pin
        self.name = name
        self.currency = currency
        self.balance = balance
    
    def to_file_string(self):
        return f"{self.account_number}|{self.pin}|{self.name}|{self.currency}|{self.balance:.2f}"
    
    @staticmethod
    def from_file_string(line):
        parts = line.strip().split('|')
        if len(parts) != 5:
            return None
        try:
            account_number = int(parts[0])
            pin = int(parts[1])
            name = parts[2]
            currency = parts[3]
            balance = float(parts[4])
            return BankAccount(account_number, pin, name, currency, balance)
        except:
            return None

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
                account = BankAccount.from_file_string(line)
                if account:
                    self.accounts.append(account)
    
    def save_accounts(self):
        with open(self.FILE_NAME, 'w') as file:
            for account in self.accounts:
                file.write(account.to_file_string() + '\n')
    
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

class CreateAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Account")
        self.setWindowIcon(QIcon(":icons/account.png"))
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout()
        
        # Form group
        form_group = QGroupBox("Account Information")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        form_layout.addRow("Name:", self.name_input)
        
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("4-digit PIN")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(4)
        form_layout.addRow("PIN:", self.pin_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def validate_input(self):
        name = self.name_input.text().strip()
        pin = self.pin_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter your name")
            return
        
        if len(pin) != 4 or not pin.isdigit():
            QMessageBox.warning(self, "Input Error", "PIN must be a 4-digit number")
            return
        
        self.accept()
    
    def get_inputs(self):
        name = self.name_input.text().strip()
        pin = int(self.pin_input.text().strip())
        return name, pin

class AccountOperationDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(":icons/bank.png"))
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        # Form group
        form_group = QGroupBox("Account Details")
        form_layout = QFormLayout()
        
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("7-digit account number")
        self.account_input.setMaxLength(7)
        form_layout.addRow("Account Number:", self.account_input)
        
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("4-digit PIN")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(4)
        form_layout.addRow("PIN:", self.pin_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def validate_input(self):
        account = self.account_input.text().strip()
        pin = self.pin_input.text().strip()
        
        if len(account) != 7 or not account.isdigit():
            QMessageBox.warning(self, "Input Error", "Account number must be a 7-digit number")
            return
        
        if len(pin) != 4 or not pin.isdigit():
            QMessageBox.warning(self, "Input Error", "PIN must be a 4-digit number")
            return
        
        self.accept()
    
    def get_inputs(self):
        account = int(self.account_input.text().strip())
        pin = int(self.pin_input.text().strip())
        return account, pin

class AmountDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(":icons/money.png"))
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        form_layout.addRow("Amount:", self.amount_input)
        
        layout.addLayout(form_layout)
        
        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def validate_input(self):
        amount = self.amount_input.text().strip()
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except:
            QMessageBox.warning(self, "Input Error", "Please enter a valid positive amount")
            return
        
        self.accept()
    
    def get_amount(self):
        return float(self.amount_input.text().strip())

class BankApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bank_system = BankSystem()
        self.initUI()
        self.setWindowIcon(QIcon(":icons/bank.png"))
    
    def initUI(self):
        self.setWindowTitle("Bank Management System")
        self.setGeometry(300, 200, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("Bank Management System")
        header_font = QFont("Arial", 18, QFont.Bold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2c3e50; padding: 15px;")
        main_layout.addWidget(header)
        
        # Create tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Operations tab
        operations_tab = QWidget()
        tab_widget.addTab(operations_tab, "Operations")
        
        # Operations layout
        operations_layout = QVBoxLayout(operations_tab)
        operations_layout.setSpacing(20)
        
        # Button group
        button_group = QGroupBox("Account Operations")
        button_layout = QVBoxLayout()
        
        # Create buttons
        buttons = [
            ("Create Account", ":icons/account.png", self.create_account),
            ("Display Accounts", ":icons/list.png", self.display_accounts),
            ("Deposit Money", ":icons/deposit.png", self.deposit_money),
            ("Withdraw Money", ":icons/withdraw.png", self.withdraw_money),
            ("Check Balance", ":icons/balance.png", self.check_balance),
            ("Delete Account", ":icons/delete.png", self.delete_account)
        ]
        
        for text, icon_path, callback in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))
            btn.setFixedHeight(50)
            btn.setStyleSheet(
                "QPushButton { background-color: #3498db; color: white; font-weight: bold; border-radius: 5px; }"
                "QPushButton:hover { background-color: #2980b9; }"
            )
            btn.clicked.connect(callback)
            button_layout.addWidget(btn)
        
        button_group.setLayout(button_layout)
        operations_layout.addWidget(button_group)
        
        # Accounts tab
        accounts_tab = QWidget()
        tab_widget.addTab(accounts_tab, "View Accounts")
        
        # Accounts layout
        accounts_layout = QVBoxLayout(accounts_tab)
        
        # Accounts list
        self.accounts_list = QListWidget()
        self.accounts_list.setStyleSheet(
            "QListWidget { background-color: #f9f9f9; border: 1px solid #ddd; }"
            "QListWidget::item { padding: 10px; border-bottom: 1px solid #eee; }"
            "QListWidget::item:selected { background-color: #e1f0fa; }"
        )
        self.update_accounts_list()
        
        accounts_layout.addWidget(self.accounts_list)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
    
    def create_account(self):
        dialog = CreateAccountDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, pin = dialog.get_inputs()
            new_account = self.bank_system.create_account(pin, name)
            self.status_bar.showMessage(f"Account created successfully! Your account number is {new_account.account_number}")
            self.update_accounts_list()
    
    def display_accounts(self):
        accounts = self.bank_system.get_all_accounts()
        if not accounts:
            QMessageBox.information(self, "No Accounts", "No accounts found in the system.")
            return
        
        # Already updated in the accounts tab, so just switch to that tab
        self.centralWidget().findChild(QTabWidget).setCurrentIndex(1)
        self.status_bar.showMessage(f"Displaying {len(accounts)} accounts")
    
    def deposit_money(self):
        dialog = AccountOperationDialog("Deposit Money", self)
        if dialog.exec_() == QDialog.Accepted:
            account_number, pin = dialog.get_inputs()
            amount_dialog = AmountDialog("Deposit Amount", self)
            if amount_dialog.exec_() == QDialog.Accepted:
                amount = amount_dialog.get_amount()
                success, message = self.bank_system.deposit(account_number, pin, amount)
                if success:
                    QMessageBox.information(self, "Success", message)
                    self.status_bar.showMessage(message)
                    self.update_accounts_list()
                else:
                    QMessageBox.warning(self, "Error", message)
    
    def withdraw_money(self):
        dialog = AccountOperationDialog("Withdraw Money", self)
        if dialog.exec_() == QDialog.Accepted:
            account_number, pin = dialog.get_inputs()
            amount_dialog = AmountDialog("Withdraw Amount", self)
            if amount_dialog.exec_() == QDialog.Accepted:
                amount = amount_dialog.get_amount()
                success, message = self.bank_system.withdraw(account_number, pin, amount)
                if success:
                    QMessageBox.information(self, "Success", message)
                    self.status_bar.showMessage(message)
                    self.update_accounts_list()
                else:
                    QMessageBox.warning(self, "Error", message)
    
    def check_balance(self):
        dialog = AccountOperationDialog("Check Balance", self)
        if dialog.exec_() == QDialog.Accepted:
            account_number, pin = dialog.get_inputs()
            success, result = self.bank_system.get_balance(account_number, pin)
            if success:
                account = self.bank_system.find_account(account_number)
                QMessageBox.information(
                    self, 
                    "Account Balance", 
                    f"Account Holder: {account.name}\n"
                    f"Account Number: {account.account_number}\n"
                    f"Current Balance: {account.currency}{result:.2f}"
                )
                self.status_bar.showMessage(f"Balance checked for account {account_number}")
            else:
                QMessageBox.warning(self, "Error", result)
    
    def delete_account(self):
        dialog = AccountOperationDialog("Delete Account", self)
        if dialog.exec_() == QDialog.Accepted:
            account_number, pin = dialog.get_inputs()
            success, message = self.bank_system.delete_account(account_number, pin)
            if success:
                QMessageBox.information(self, "Success", message)
                self.status_bar.showMessage(message)
                self.update_accounts_list()
            else:
                QMessageBox.warning(self, "Error", message)
    
    def update_accounts_list(self):
        self.accounts_list.clear()
        accounts = self.bank_system.get_all_accounts()
        
        if not accounts:
            item = QListWidgetItem("No accounts found")
            item.setTextAlignment(Qt.AlignCenter)
            self.accounts_list.addItem(item)
            return
        
        for account in accounts:
            item_text = (
                f"Account: {account.account_number} | "
                f"Name: {account.name} | "
                f"Balance: {account.currency}{account.balance:.2f}"
            )
            item = QListWidgetItem(item_text)
            self.accounts_list.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = BankApp()
    window.show()
    
    sys.exit(app.exec_())