# SecureVault — Secure Password Manager

A complete Python Flask password manager project for a cybersecurity coursework/demo submission.

## What it does

- User registration and login
- Master-password-based vault unlocking
- Secure credential storage using authenticated encryption
- Password generator using Python's `secrets` module
- SQLite database storage
- Web interface for adding, viewing, editing, deleting, and searching credentials
- CSRF protection for forms
- SQL injection resistance through SQLAlchemy parameterized queries
- XSS reduction through Jinja autoescaping and strict template handling
- Basic browser security headers

## Security design

This project avoids the lazy weak design of storing one global encryption key in the source code.

For each user:

1. The login password is hashed using Werkzeug's password hashing.
2. A random per-user encryption salt is stored in the database.
3. On login, PBKDF2-HMAC-SHA256 derives a Fernet-compatible vault key from the master password and salt.
4. Credential fields are encrypted with Fernet before being saved to SQLite.
5. The derived vault key is kept only in a server-side session and cleared on logout/session expiry.

This is good for an academic demo. For real production use, you would still need HTTPS, audited deployment, rate limiting, account recovery design, key rotation, backup strategy, and stronger operational controls.

## Requirements

Install these before running:

- Python 3.11 or newer recommended
- VS Code
- Git optional

## Run on Windows PowerShell

```powershell
cd secure_password_manager
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

## Run on macOS/Linux

```bash
cd secure_password_manager
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

## Recommended demo flow

1. Create a new account.
2. Log in with the master password.
3. Open the password generator.
4. Generate a strong password and copy it.
5. Add a credential, paste the generated password, and save.
6. View the saved credential and use the copy button.
7. Edit the credential.
8. Delete the credential.
9. Log out and explain that the vault key is cleared.

## Project structure

```text
secure_password_manager/
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
├── requirements.txt
├── run.py
├── SECURITY_NOTES.md
└── USER_GUIDE.md
```

## Reset the database

Stop the server, then delete the `instance` folder. It will be recreated automatically next time you run the app.

## Important limitation

This is a local educational project. Do not deploy it publicly without hardening it first.
