# SecureVault: Secure Password Manager

SecureVault is a local web-based password manager built with Python, Flask, SQLite, and the `cryptography` library. It was developed for a cybersecurity coursework/demo submission.

The application allows users to create an account, unlock a personal vault using a master password, generate strong passwords, and store website credentials encrypted in a local SQLite database.

## What it does

* User registration and login
* Master-password-based vault unlocking
* Secure credential storage using authenticated encryption
* Password generator using Python's `secrets` module
* SQLite database storage
* Web interface for adding, viewing, editing, deleting, and searching credentials
* CSRF protection for forms
* SQL injection resistance through SQLAlchemy database queries
* XSS reduction through Jinja template escaping
* Basic browser security headers
* Automated tests for important app and encryption behavior

## Security design

This project avoids the weak design of storing one global encryption key directly in the source code.

For each user:

1. The login password is hashed using Werkzeug password hashing.
2. A random per-user encryption salt is stored in the database.
3. On login, PBKDF2-HMAC-SHA256 derives a Fernet-compatible vault key from the master password and salt.
4. Credential fields are encrypted with Fernet before being saved to SQLite.
5. The derived vault key is kept only in the server-side session and is cleared on logout/session expiry.

This is suitable for an academic demonstration. For real production use, the project would still need HTTPS-only deployment, rate limiting, audited hosting, stronger operational key management, secure backups, recovery design, logging, monitoring, and a full security review.

## Requirements

Install these before running:

* Python 3.11 or newer
* Git, recommended for cloning the repository
* VS Code, optional but recommended

## Run on Windows PowerShell

Clone the repository and enter the project folder:

```powershell
git clone https://github.com/raifkhatib/SecureVault-Password-Manager.git
cd SecureVault-Password-Manager
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies inside the virtual environment:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the application:

```powershell
python run.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

If PowerShell blocks virtual environment activation, run this once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Run on Windows CMD

Clone the repository and enter the project folder:

```cmd
git clone https://github.com/raifkhatib/SecureVault-Password-Manager.git
cd SecureVault-Password-Manager
```

Create and activate a virtual environment:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Install dependencies inside the virtual environment:

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the application:

```cmd
python run.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

## Run on macOS/Linux

Clone the repository and enter the project folder:

```bash
git clone https://github.com/raifkhatib/SecureVault-Password-Manager.git
cd SecureVault-Password-Manager
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the application:

```bash
python run.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

## Run tests

After installing the dependencies, run:

```powershell
python -m pytest
```

Expected result:

```text
3 passed
```

Warnings from third-party packages may appear, but they do not mean the tests failed.

## Recommended demo flow

1. Open the GitHub repository.
2. Clone or download the project.
3. Create and activate a virtual environment.
4. Install dependencies using `requirements.txt`.
5. Run tests with `python -m pytest`.
6. Run the app with `python run.py`.
7. Open `http://127.0.0.1:5000`.
8. Create a new account.
9. Log in with the master password.
10. Open the password generator.
11. Generate a strong password and copy it.
12. Add a credential using the generated password.
13. View the saved credential.
14. Edit the credential.
15. Search for the credential.
16. Delete a test credential if needed.
17. Log out and explain that the vault key is cleared from the session.
18. Log in again to show that saved credentials persist in the database.

## Project structure

```text
SecureVault-Password-Manager/
├── app/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   └── security.py
├── tests/
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── run.py
├── README.md
├── SECURITY_NOTES.md
└── USER_GUIDE.md
```

## Database behavior

The SQLite database is created locally when the app runs. Local database files and runtime folders are ignored by Git so they are not pushed to the repository.

To reset the database:

1. Stop the server.
2. Delete the `instance` folder.
3. Run the app again.

The app will recreate the local database automatically.

## Assignment requirement coverage

| Requirement                              | Implementation                                     |
| ---------------------------------------- | -------------------------------------------------- |
| User registration and authentication     | Flask routes, forms, Flask-Login, password hashing |
| Secure password storage using encryption | Fernet authenticated encryption                    |
| Password generation                      | Python `secrets` module                            |
| Password retrieval and management        | Vault web interface                                |
| Database for encrypted credentials       | SQLite with SQLAlchemy                             |
| Python backend                           | Python Flask                                       |
| Proper encryption for sensitive data     | `cryptography` package                             |
| Password hashing and salting             | Werkzeug password hashing and per-user vault salt  |
| SQL injection protection                 | SQLAlchemy queries                                 |
| XSS protection                           | Jinja autoescaping                                 |
| CSRF protection                          | Flask-WTF CSRF tokens                              |
| Demo/documentation                       | README, USER_GUIDE.md, SECURITY_NOTES.md           |

## Important limitation

This is a local educational project. Do not deploy it publicly without hardening it first.
