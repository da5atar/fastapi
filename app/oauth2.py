from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from app import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "7e38d8e88b36fc6aac4f0f6f9907f39b3659a7b661818c6552ac6aaf490e52d90"
ALGORITHM = "HS256"
EXPIRATION_TIME = 30  # minutes


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        # print(expire)
    else:
        expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception: Exception):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "exp" in decoded_jwt:
            now = datetime.utcnow()
            exp = datetime.utcfromtimestamp(decoded_jwt["exp"])
            # print(now, exp)
            if now >= exp:
                raise ExpiredSignatureError("Token has expired")
        # print(decoded_jwt)
        user_credentials = schemas.TokenData(user_id=decoded_jwt["sub"])
        # print(user_credentials)
    except JWTError or JWTClaimsError as e:
        print(e)
        raise credentials_exception
    return user_credentials


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
