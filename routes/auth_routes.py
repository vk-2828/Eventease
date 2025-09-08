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



# from fastapi import APIRouter, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from database import db
# from schemas.user import UserCreate
# from auth import hash_password, verify_password, create_access_token
# from config import JWT_SECRET, JWT_ALGORITHM  # ✅ import from config

# router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# @router.post("/signup")
# async def register(user: UserCreate):
#     existing = await db.users.find_one({"email": user.email})
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     user_doc = user.dict()
#     user_doc["password"] = hash_password(user_doc.pop("password"))
#     res = await db.users.insert_one(user_doc)
#     return {"id": str(res.inserted_id), "email": user.email}

# @router.post("/signin")
# async def login(user: UserCreate):
#     db_user = await db.users.find_one({"email": user.email})
#     if not db_user or not verify_password(user.password, db_user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({
#         "sub": db_user["email"],
#         "roles": db_user.get("roles", ["participant"])
#     })
#     return {"access_token": token, "token_type": "bearer"}

# # ✅ Dependency to fetch current user
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid authentication token")

#         db_user = await db.users.find_one({"email": email})
#         if not db_user:
#             raise HTTPException(status_code=401, detail="User not found")

#         return {
#             "email": db_user["email"],
#             "roles": db_user.get("roles", ["participant"])
#         }

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Could not validate credentials")

# from fastapi import APIRouter, HTTPException, Depends
# from database import db
# from jose import jwt
# from schemas.user import UserCreate
# from auth import hash_password, verify_password, create_access_token
# from config import JWT_SECRET, JWT_ALGORITHM

# router = APIRouter()

# # -------------------
# # Signup
# # -------------------
# @router.post("/signup", response_model=dict)
# async def signup(user: UserCreate):
#     existing = await db.users.find_one({"email": user.email})
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     user_dict = user.dict()
#     user_dict["password"] = hash_password(user_dict.pop("password"))
#     res = await db.users.insert_one(user_dict)

#     user_info = {
#         "id": str(res.inserted_id),
#         "name": user.name,
#         "email": user.email,
#         "roles": user.roles
#     }

#     token = create_access_token({"sub": user.email, "roles": user.roles})
#     return {"user": user_info, "access_token": token, "token_type": "bearer"}

# # -------------------
# # Signin
# # -------------------
# @router.post("/signin", response_model=dict)
# async def signin(user: UserCreate):
#     db_user = await db.users.find_one({"email": user.email})
#     if not db_user or not verify_password(user.password, db_user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     user_info = {
#         "id": str(db_user["_id"]),
#         "name": db_user["name"],
#         "email": db_user["email"],
#         "roles": db_user.get("roles", ["participant"])
#     }

#     token = create_access_token({
#         "sub": db_user["email"],
#         "roles": db_user.get("roles", ["participant"])
#     })
#     return {"user": user_info, "access_token": token, "token_type": "bearer"}

# # -------------------
# # Get current user dependency
# # -------------------
# from fastapi.security import OAuth2PasswordBearer
# from fastapi import HTTPException

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid authentication token")

#         db_user = await db.users.find_one({"email": email})
#         if not db_user:
#             raise HTTPException(status_code=401, detail="User not found")

#         return {
#             "id": str(db_user["_id"]),
#             "email": db_user["email"],
#             "name": db_user["name"],
#             "roles": db_user.get("roles", ["participant"])
#         }

#     except Exception:
#         raise HTTPException(status_code=401, detail="Could not validate credentials")


# from fastapi import APIRouter, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from database import db
# from jose import jwt
# from schemas.user import UserCreate
# from pydantic import BaseModel, EmailStr
# from auth import hash_password, verify_password, create_access_token
# from config import JWT_SECRET, JWT_ALGORITHM

# router = APIRouter()

# # -------------------
# # Login schema (signin)
# # -------------------
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# # -------------------
# # Signup
# # -------------------
# @router.post("/signup", response_model=dict)
# async def signup(user: UserCreate):
#     existing = await db.users.find_one({"email": user.email})
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     user_dict = user.dict()
#     user_dict["password"] = hash_password(user_dict.pop("password"))
#     res = await db.users.insert_one(user_dict)

#     user_info = {
#         "id": str(res.inserted_id),
#         "name": user.name,
#         "email": user.email,
#         "roles": user.roles
#     }

#     token = create_access_token({"sub": user.email, "roles": user.roles})
#     return {"user": user_info, "access_token": token, "token_type": "bearer"}

# # -------------------
# # Signin
# # -------------------
# @router.post("/signin", response_model=dict)
# async def signin(user: UserLogin):
#     db_user = await db.users.find_one({"email": user.email})
#     if not db_user or not verify_password(user.password, db_user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     user_info = {
#         "id": str(db_user["_id"]),
#         "name": db_user["name"],
#         "email": db_user["email"],
#         "roles": db_user.get("roles", ["participant"])
#     }

#     token = create_access_token({
#         "sub": db_user["email"],
#         "roles": db_user.get("roles", ["participant"])
#     })

#     return {"user": user_info, "access_token": token, "token_type": "bearer"}


# # -------------------
# # Get current user dependency
# # -------------------
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid authentication token")

#         db_user = await db.users.find_one({"email": email})
#         if not db_user:
#             raise HTTPException(status_code=401, detail="User not found")

#         return {
#             "id": str(db_user["_id"]),
#             "email": db_user["email"],
#             "name": db_user["name"],
#             "roles": db_user.get("roles", ["participant"])
#         }

#     except Exception:
#         raise HTTPException(status_code=401, detail="Could not validate credentials")




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
