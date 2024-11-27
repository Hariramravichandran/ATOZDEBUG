from fastapi import APIRouter, HTTPException, Response
from auth.models import User
from auth.utils import hash_password, verify_password, create_access_token
from db import users_collection

router = APIRouter()

@router.post("/register/")
def register(user: User):
    
    user_exists = users_collection.find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.password = hash_password(user.password)
    users_collection.insert_one(user.dict())
    
    token = create_access_token(user.email, user.role, remember_me=False)
    user_data = {"email": user.email, "role": user.role}
    return {"message": "User registered successfully", "token": token, "user": user_data}

@router.post("/login/")
def login(user: User, response: Response, remember_me: bool = False):
    
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email, db_user["role"], remember_me)
    user_data = {"email": db_user["email"], "role": db_user["role"]}
    
    response.set_cookie("session_token", token, httponly=True)
    return {"message": "Login successful", "token": token, "user": user_data}

@router.post("/logout/")
def logout(response: Response):
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}
