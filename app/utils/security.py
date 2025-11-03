from jose import JWTError, jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from cryptography.fernet import Fernet
import os

# JWT settings
SECRET_KEY = "your-secret-key-keep-it-secret"  # In production, use environment variable
ALGORITHM = "HS256"

# File encryption key
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

security = HTTPBearer()

def encrypt_file(file_data: bytes) -> bytes:
    """Encrypt file data"""
    return cipher_suite.encrypt(file_data)

def decrypt_file(encrypted_data: bytes) -> bytes:
    """Decrypt file data"""
    return cipher_suite.decrypt(encrypted_data)

def create_access_token(data: dict):
    """Create JWT token"""
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )