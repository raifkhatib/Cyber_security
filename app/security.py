import base64
import secrets
import string
from dataclasses import dataclass

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ITERATIONS = 600_000


def derive_vault_key(master_password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from the user's master password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode("utf-8")))


def encrypt_text(vault_key: bytes, value: str | None) -> str:
    clean_value = value or ""
    return Fernet(vault_key).encrypt(clean_value.encode("utf-8")).decode("utf-8")


def decrypt_text(vault_key: bytes, token: str | None) -> str:
    if not token:
        return ""
    try:
        return Fernet(vault_key).decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise ValueError("The vault key could not decrypt this value.") from exc


@dataclass
class PasswordOptions:
    length: int = 20
    use_uppercase: bool = True
    use_lowercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True


def generate_secure_password(options: PasswordOptions) -> str:
    pools: list[str] = []
    required_chars: list[str] = []

    if options.use_uppercase:
        pools.append(string.ascii_uppercase)
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if options.use_lowercase:
        pools.append(string.ascii_lowercase)
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if options.use_digits:
        pools.append(string.digits)
        required_chars.append(secrets.choice(string.digits))
    if options.use_symbols:
        symbols = "!@#$%^&*()-_=+[]{};:,.?/"
        pools.append(symbols)
        required_chars.append(secrets.choice(symbols))

    if not pools:
        raise ValueError("At least one character type must be selected.")

    length = max(options.length, len(required_chars), 8)
    all_chars = "".join(pools)
    remaining = [secrets.choice(all_chars) for _ in range(length - len(required_chars))]
    password_chars = required_chars + remaining

    # Fisher-Yates shuffle using a cryptographically secure random index.
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)
