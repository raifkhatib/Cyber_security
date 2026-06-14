# Security Notes

## What is protected

The following credential fields are encrypted before storage:

- Service name
- Login name / email
- Password
- URL
- Private notes

The database does not store plaintext credentials.

## Password hashing

User login passwords are not stored directly. The application uses Werkzeug password hashing through `generate_password_hash` and `check_password_hash`.

## Vault encryption

The vault key is derived from the user's master password and a random per-user salt using PBKDF2-HMAC-SHA256 with 600,000 iterations.

The derived key is used with Fernet authenticated encryption from the `cryptography` package.

## Session handling

The derived vault key is stored in a server-side session, not inside the SQLite database and not directly inside a browser-readable cookie. It is cleared on logout and expires after 30 minutes.

## SQL injection protection

The project uses SQLAlchemy ORM queries instead of building SQL strings manually. This prevents the common beginner mistake of concatenating user input into SQL.

## XSS protection

Jinja templates escape variables by default. The project does not render user input with `safe` or inject it as raw HTML.

## CSRF protection

Forms use Flask-WTF CSRF tokens. Destructive actions such as logout and delete are POST-only and CSRF-protected.

## Security headers

The app sets basic security headers including:

- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy

## Honest limitations

This project is solid for coursework, but it is not a production-grade password manager. A real production product would need:

- HTTPS-only deployment
- Secure secret management
- Rate limiting and lockout protection
- Audit logging
- Backups and recovery design
- Key rotation
- Penetration testing
- More detailed threat modeling
- Protection against malware on the user's device
