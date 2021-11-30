from datetime import datetime, timedelta

from jose import JWTError, jwt

SECRET_KEY = "7e38d8e88b36fc6aac4f0f6f9907f39b3659a7b661818c6552ac6aaf490e52d90"
ALGORITHM = "HS256"
EXPIRATION_TIME = 30 # minutes

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
