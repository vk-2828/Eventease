# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from database import db
# from models.helpers import user_helper
# from schemas.user import UserCreate, UserOut
# from auth import hash_password, verify_password, create_access_token

# router = APIRouter()

# @router.post("/register", response_model=UserOut)
# async def register(user: UserCreate):
#     existing_user = await db.users.find_one({"email": user.email})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     user_dict = user.dict()
#     user_dict["password"] = hash_password(user.password)
#     result = await db.users.insert_one(user_dict)
#     return user_helper(await db.users.find_one({"_id": result.inserted_id}))

# @router.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await db.users.find_one({"email": form_data.username})
#     if not user or not verify_password(form_data.password, user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": user["email"], "roles": user.get("roles", ["participant"])})
#     return {"access_token": token, "token_type": "bearer"}



from fastapi import APIRouter, HTTPException
from database import db
from bson import ObjectId
from schemas.user import UserOut

router = APIRouter()

# -------------------
# Get all users
# -------------------
@router.get("/", response_model=list[UserOut])
async def get_all_users():
    users = []
    async for u in db.users.find():
        users.append({
            "id": str(u["_id"]),
            "name": u["name"],
            "email": u["email"],
            "roles": u.get("roles", ["participant"])
        })
    return users

# -------------------
# Get user by ID
# -------------------
@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "roles": user.get("roles", ["participant"])
    }

# -------------------
# Update user
# -------------------
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, updated_data: dict):
    if "password" in updated_data:
        from auth import hash_password
        updated_data["password"] = hash_password(updated_data["password"])

    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "roles": user.get("roles", ["participant"])
    }

# -------------------
# Delete user
# -------------------
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
