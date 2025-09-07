# from fastapi import APIRouter
# # import List
# from database import db
# from models.helpers import registration_helper
# from schemas.registration import RegistrationCreate, RegistrationOut
# from datetime import datetime

# router = APIRouter()

# @router.post("/", response_model=RegistrationOut)
# async def register_event(reg: RegistrationCreate):
#     reg_dict = reg.dict()
#     reg_dict["created_at"] = datetime.utcnow()
#     result = await db.registrations.insert_one(reg_dict)
#     return registration_helper(await db.registrations.find_one({"_id": result.inserted_id}))

from fastapi import APIRouter, HTTPException
from typing import List
from database import db
from models.helpers import registration_helper
from schemas.registration import RegistrationCreate, RegistrationOut
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=RegistrationOut)
async def register_event(reg: RegistrationCreate):
    reg_dict = reg.dict()
    reg_dict["created_at"] = datetime.utcnow()
    result = await db.registrations.insert_one(reg_dict)
    return registration_helper(await db.registrations.find_one({"_id": result.inserted_id}))


@router.get("/{event_id}", response_model=List[RegistrationOut])
async def get_registrations_for_event(event_id: str):
    # Validate the event_id format
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid Event ID format")

    # Fetch all registrations with the matching event_id
    registrations = []
    async for reg in db.registrations.find({"event_id": event_id}):
        registrations.append(registration_helper(reg))
    
    return registrations