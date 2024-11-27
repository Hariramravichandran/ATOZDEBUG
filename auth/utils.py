from passlib.context import CryptContext
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY
from db import users_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(email: str, role: str, remember_me: bool) -> str:
    expire = datetime.utcnow() + (timedelta(days=7) if remember_me else timedelta(hours=1))
    to_encode = {"exp": expire, "email": email, "role": role}
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def get_current_user(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")
        role = payload.get("role")
        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "role": role}
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
