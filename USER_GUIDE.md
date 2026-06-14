# SecureVault User Guide

## Purpose

SecureVault is a simple web-based password manager. It lets a user create an account, unlock an encrypted vault, generate strong passwords, and save credentials securely in a local SQLite database.

## How to run

1. Open the project folder in VS Code.
2. Open the terminal inside VS Code.
3. Create a Python virtual environment.
4. Install the required packages from `requirements.txt`.
5. Run `python run.py`.
6. Open `http://127.0.0.1:5000` in the browser.

## How to use

### 1. Create an account

Click **Create account**, enter a username, and choose a strong master password.

The master password is important because it unlocks the encrypted vault. If it is lost, the encrypted credentials cannot be recovered.

### 2. Log in

Click **Login**, enter the username and master password, then unlock the vault.

### 3. Generate a password

Open **Generator**, choose the password length and character types, then click **Generate password**.

Copy the generated password and use it when creating a new credential.

### 4. Add a credential

Open **Add credential** and fill in:

- Service name
- Username or email
- Password
- Website URL
- Private notes

Click **Save credential**. The data is encrypted before it is stored in the database.

### 5. View and manage credentials

From the vault dashboard, click **View** to see a saved credential. You can copy the username or password, edit the entry, or delete it.

### 6. Log out

Click **Logout** when finished. This clears the active vault key from the session.

## What to show in a demo video

1. Start the Flask server.
2. Register a user.
3. Log in.
4. Generate a password.
5. Add a credential.
6. View and copy the password.
7. Edit the saved credential.
8. Delete the credential.
9. Log out.

## Security features to mention

- Password hashing and salting
- Per-user encryption salt
- PBKDF2 key derivation
- Fernet authenticated encryption
- CSRF protection
- SQLAlchemy parameterized database queries
- Jinja autoescaping against XSS
- Security headers
