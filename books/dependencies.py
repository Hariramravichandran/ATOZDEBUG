from fastapi import Depends, HTTPException
from auth.utils import get_current_user

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def member_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "member"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return current_user
