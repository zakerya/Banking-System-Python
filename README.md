# Bank Management System - Web App

## Overview
The Bank Management System is a secure, user-friendly desktop application built with Python, HTML, CSS and JavaScript that simulates core banking operations. This system allows users to create accounts, perform transactions, manage funds, and view account details with robust data persistence.

## Key Features

### Account Management
- Create new bank accounts with unique 7-digit numbers
- Delete accounts securely with PIN verification
- View all accounts with balances

### Financial Operations
- Deposit funds to accounts
- Withdraw money with balance validation
- Check account balances instantly

### Security
- 4-digit PIN authentication for all transactions
- Secure data storage with encrypted PINs
- Input validation for all operations

### User Experience
- Intuitive tabbed interface
- Responsive design with visual feedback
- Professional banking workflow
- Status notifications and error handling

## Technical Specifications

### Requirements
- Python 3.7+
- PyQt5
- Operating System: Windows, macOS, Linux

## Data Persistence
Account data is stored in `bank.dat` using a pipe-delimited format:

```
accountNumber|pin|name|currency|balance
```

## Usage Guide

### Creating an Account
1. Click "Create Account"
2. Enter your full name
3. Set a 4-digit PIN
4. System generates unique account number

### Performing Transactions
1. Select operation (Deposit/Withdraw/Check Balance/Delete)
2. Enter 7-digit account number
3. Verify with 4-digit PIN
4. Enter amount (for deposits/withdrawals)
5. Confirm operation

### Viewing Accounts
Navigate to "View Accounts" tab to see all accounts with:
- Account numbers
- Account holder names
- Current balances
- Currency symbols

## Technology Stack
- **Frontend**: HTML, CSS & JavaScript
- **Backend**: Python
- **Data Storage**: Flat-file system with custom serialization
- **Security**: PIN-based authentication

## Benefits
- 💰 **Real Banking Simulation**: Experience actual banking operations
- 🔒 **Secure**: PIN-protected transactions
- 💾 **Persistent Storage**: Accounts survive application restarts
- 🖥️ **Cross-Platform**: Runs on Windows, macOS, and Linux
- 🚀 **Efficient**: Lightweight with minimal dependencies
