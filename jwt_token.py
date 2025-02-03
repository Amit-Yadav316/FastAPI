from fastapi import HTTPException,status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
import logging
from schemas import TokenData
from jose import JWTError, jwt


SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        token_data=TokenData(email=email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credential"
        )


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logging.info(f"Decoded Payload: {payload}")
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
