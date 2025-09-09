from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database import db
from jose import jwt
from schemas.user import UserCreate
from pydantic import BaseModel, EmailStr
from auth import hash_password, verify_password, create_access_token
from config import JWT_SECRET, JWT_ALGORITHM

router = APIRouter()

# -------------------
# Login schema (signin)
# -------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# -------------------
# Signup
# -------------------
@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user_dict.pop("password"))
    res = await db.users.insert_one(user_dict)

    user_info = {
        "id": str(res.inserted_id),
        "name": user.name,
        "email": user.email,
        "roles": user.roles
    }

    token = create_access_token({
        "sub": str(res.inserted_id),       # store user id
        "email": user.email,               # ✅ include email for /me
        "roles": user.roles
    })
    return {"user": user_info, "access_token": token, "token_type": "bearer"}


# -------------------
# Signin
# -------------------
@router.post("/signin", response_model=dict)
async def signin(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_info = {
        "id": str(db_user["_id"]),
        "name": db_user["name"],
        "email": db_user["email"],
        "roles": db_user.get("roles", ["participant"])
    }

    token = create_access_token({
        "sub": str(db_user["_id"]),        # store user id
        "email": db_user["email"],         # ✅ include email for /me
        "roles": db_user.get("roles", ["participant"])
    })

    return {"user": user_info, "access_token": token, "token_type": "bearer"}


# -------------------
# Get current user dependency
# -------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("email")   # ✅ get email from token
        if email is None:
            raise HTTPException(status_code=401, detail="Token missing email")

        db_user = await db.users.find_one({"email": email})
        if not db_user:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "id": str(db_user["_id"]),
            "email": db_user["email"],
            "name": db_user["name"],
            "roles": db_user.get("roles", ["participant"])
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
