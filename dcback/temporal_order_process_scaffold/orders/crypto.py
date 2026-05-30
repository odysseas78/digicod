from django.conf import settings
from cryptography.fernet import Fernet

def _fernet() -> Fernet:
    key = getattr(settings, "CODE_ENCRYPTION_KEY", "")
    if not key:
        raise RuntimeError("CODE_ENCRYPTION_KEY is not configured")
    return Fernet(key.encode() if isinstance(key, str) else key)

def encrypt_text(value: str | None) -> str:
    if not value:
        return ""
    return _fernet().encrypt(value.encode("utf-8")).decode("utf-8")

def decrypt_text(value: str | None) -> str:
    if not value:
        return ""
    return _fernet().decrypt(value.encode("utf-8")).decode("utf-8")
