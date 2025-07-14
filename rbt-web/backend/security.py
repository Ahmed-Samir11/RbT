import time
import hashlib
import os
from functools import wraps
from fastapi import HTTPException, Request, status
import jwt

JWT_SECRET = os.environ.get("JWT_SECRET", "supersecret")
JWT_ALGORITHM = "HS256"
RATE_LIMIT = 100  # requests per hour
RATE_LIMIT_WINDOW = 3600  # seconds

# In-memory rate limiter: {user_id: [timestamps]}
RATE_LIMIT_STORE = {}

# --- JWT Auth ---
def create_jwt(payload):
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Rate Limiting ---
def rate_limiter(user_id):
    now = time.time()
    timestamps = RATE_LIMIT_STORE.get(user_id, [])
    # Remove timestamps outside the window
    timestamps = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    timestamps.append(now)
    RATE_LIMIT_STORE[user_id] = timestamps

# --- GDPR Anonymization ---
def anonymize_data(record, salt="rbt-salt"):
    # Pseudonymize user_id, minimize location
    user_id = record.get("user_id", "")
    city = record.get("city", "")
    country = record.get("country", "")
    hashed_id = hashlib.sha256((str(user_id) + salt).encode()).hexdigest()
    return {
        **record,
        "user_id": hashed_id,
        "location": f"{city}, {country}"
    }
