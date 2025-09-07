from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import db
from models.helpers import user_helper
from schemas.user import UserCreate, UserOut
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    result = await db.users.insert_one(user_dict)
    return user_helper(await db.users.find_one({"_id": result.inserted_id}))

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"], "roles": user.get("roles", ["participant"])})
    return {"access_token": token, "token_type": "bearer"}
