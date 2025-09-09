from fastapi import APIRouter, Depends, HTTPException
from database import db
from bson import ObjectId
from schemas.registration import RegistrationCreate, RegistrationOut
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import JWT_SECRET, JWT_ALGORITHM
from typing import List
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")


# -------------------
# Decode token (now includes email)
# -------------------
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import JWT_SECRET, JWT_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")

def get_user_info(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("email")
        roles: list = payload.get("roles", [])

        if email is None:
            raise HTTPException(status_code=401, detail="Token missing email")

        return {
            "id": payload.get("sub"),
            "email": email,
            "roles": roles
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



# -------------------
# Helper to serialize ObjectId
# -------------------
def registration_helper(registration) -> dict:
    return {
        "id": str(registration["_id"]),
        "event_id": str(registration["event_id"]),
        "user_id": registration["user_id"],
        "name": registration["name"],
        "email": registration["email"],
        "college": registration.get("college", ""),
        "phone": registration.get("phone", ""),
        "created_at": registration["created_at"].isoformat()
    }


# -------------------
# Register for an event
# -------------------
@router.post("/", response_model=RegistrationOut)
async def register_event(registration: RegistrationCreate, user=Depends(get_user_info)):
    if "participant" not in user["roles"]:
        raise HTTPException(status_code=403, detail="Only participants can register")

    existing = await db.registrations.find_one({
        "user_id": user["id"],
        "event_id": registration.event_id
    })
    if existing:
        raise HTTPException(status_code=400, detail="Already registered for this event")

    registration_dict = registration.dict()
    registration_dict.update({
        "user_id": user["id"],
        "email": user["email"],               # ✅ store email in registration
        "created_at": datetime.utcnow()
    })

    result = await db.registrations.insert_one(registration_dict)
    saved = await db.registrations.find_one({"_id": result.inserted_id})
    return registration_helper(saved)


@router.get("/me", response_model=List[dict])
async def my_registrations(user=Depends(get_user_info)):
    print("🔑 User Info from Token:", user)  # ✅ full user dict
    
    if "participant" not in user["roles"]:
        raise HTTPException(status_code=403, detail="Only participants can view their registrations")

    print("📧 Participant Email:", user['email'])

    pipeline = [
        {"$match": {"email": user["email"]}},   # ✅ email match
        {"$addFields": {"eventObjId": {"$toObjectId": "$event_id"}}},
        {"$lookup": {
            "from": "events",
            "localField": "eventObjId",
            "foreignField": "_id",
            "as": "event_details"
        }},
        {"$unwind": "$event_details"},
        {"$project": {
    "_id": 0,
    "registration_id": {"$toString": "$_id"},
    "email": 1,
    "name": 1,
    "event_id": 1,
    "college": 1,
    "phone": 1,
    "created_at": 1,
    "event_details.id": {"$toString": "$event_details._id"},  # ✅ add this
    "event_details.title": 1,
    "event_details.date": 1,
    "event_details.venue": 1,
    "event_details.description": 1,
    "event_details.schedule": 1,
    "event_details.rules": 1,
    "event_details.contact": 1
}}

    ]

    print("📌 Running Aggregation Pipeline:", pipeline)

    results = await db.registrations.aggregate(pipeline).to_list(length=None)

    print("✅ Aggregation Results:", results)

    return results