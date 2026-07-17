from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """
    return password_hash.hash(password)


# Backward-compatible alias
def get_password_hash(password: str) -> str:
    return hash_password(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against its hash.
    """
    return password_hash.verify(password, hashed_password)