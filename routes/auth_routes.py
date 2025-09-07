# from fastapi import APIRouter, HTTPException
# from database import db
# from schemas.user import UserCreate
# from auth import hash_password, verify_password, create_access_token

# router = APIRouter()

# @router.post("/register")
# async def register(user: UserCreate):
#     existing = await db.users.find_one({"email": user.email})
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     user_doc = user.dict()
#     user_doc["password"] = hash_password(user_doc.pop("password"))
#     res = await db.users.insert_one(user_doc)
#     return {"id": str(res.inserted_id), "email": user.email}

# @router.post("/login")
# async def login(user: UserCreate):
#     db_user = await db.users.find_one({"email": user.email})
#     if not db_user or not verify_password(user.password, db_user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": db_user["email"], "roles": db_user.get("roles", ["participant"])})
#     return {"access_token": token, "token_type": "bearer"}



from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import db
from schemas.user import UserCreate
from auth import hash_password, verify_password, create_access_token
from config import JWT_SECRET, JWT_ALGORITHM  # ✅ import from config

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/register")
async def register(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = user.dict()
    user_doc["password"] = hash_password(user_doc.pop("password"))
    res = await db.users.insert_one(user_doc)
    return {"id": str(res.inserted_id), "email": user.email}

@router.post("/login")
async def login(user: UserCreate):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": db_user["email"],
        "roles": db_user.get("roles", ["participant"])
    })
    return {"access_token": token, "token_type": "bearer"}

# ✅ Dependency to fetch current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        db_user = await db.users.find_one({"email": email})
        if not db_user:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "email": db_user["email"],
            "roles": db_user.get("roles", ["participant"])
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

