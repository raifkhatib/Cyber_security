from app.security import PasswordOptions, decrypt_text, derive_vault_key, encrypt_text, generate_secure_password


def test_encrypt_decrypt_round_trip():
    key = derive_vault_key("CorrectHorseBatteryStaple", b"1234567890abcdef")
    token = encrypt_text(key, "secret-password")

    assert token != "secret-password"
    assert decrypt_text(key, token) == "secret-password"


def test_generator_respects_minimum_length_and_character_types():
    password = generate_secure_password(
        PasswordOptions(length=16, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True)
    )

    assert len(password) == 16
    assert any(ch.isupper() for ch in password)
    assert any(ch.islower() for ch in password)
    assert any(ch.isdigit() for ch in password)
    assert any(not ch.isalnum() for ch in password)
