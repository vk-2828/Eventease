from fastapi import APIRouter, Depends, HTTPException
from database import db
from bson import ObjectId
from models.helpers import event_helper, user_helper
from schemas.event import EventCreate, EventOut
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import JWT_SECRET, JWT_ALGORITHM
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

# Utility to decode token and get roles
async def get_roles(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("roles", [])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -------------------
# Create Event (Organizer Only)
# -------------------
@router.post("/", response_model=EventOut)
async def create_event(event: EventCreate, roles: list = Depends(get_roles)):
    if "organizer" not in roles:
        raise HTTPException(status_code=403, detail="Only organizers can create events")
    
    result = await db.events.insert_one(event.dict())
    return event_helper(await db.events.find_one({"_id": result.inserted_id}))

# -------------------
# List all events (Everyone)
# -------------------
@router.get("/", response_model=list[EventOut])
async def list_events():
    events = []
    async for event in db.events.find():
        events.append(event_helper(event))
    return events

# -------------------
# Get single event (Everyone)
# -------------------
@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: str):
    event = await db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event_helper(event)

# -------------------
# Get participants of an event (Organizer Only)
# -------------------
@router.get("/{event_id}/participants", response_model=List[dict])
async def get_event_participants(event_id: str, roles: list = Depends(get_roles)):
    if "organizer" not in roles:
        raise HTTPException(status_code=403, detail="Only organizers can view participants")
    
    participants = []

    async for registration in db.registrations.find({"event_id": event_id}):
        participant_info = {
            "name": registration.get("name"),
            "email": registration.get("email"),
            "phone": registration.get("phone"),
            "college": registration.get("college")
        }
        participants.append(participant_info)
    
    return participants

# -------------------
# Edit Event (Organizer Only)
# -------------------
@router.put("/{event_id}", response_model=EventOut)
async def edit_event(event_id: str, updated_event: EventCreate, roles: list = Depends(get_roles)):
    if "organizer" not in roles:
        raise HTTPException(status_code=403, detail="Only organizers can edit events")
    
    event = await db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    await db.events.update_one({"_id": ObjectId(event_id)}, {"$set": updated_event.dict()})
    updated = await db.events.find_one({"_id": ObjectId(event_id)})
    return event_helper(updated)

# -------------------
# Delete Event (Organizer Only)
# -------------------
@router.delete("/{event_id}")
async def delete_event(event_id: str, roles: list = Depends(get_roles)):
    if "organizer" not in roles:
        raise HTTPException(status_code=403, detail="Only organizers can delete events")
    
    event = await db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    await db.events.delete_one({"_id": ObjectId(event_id)})
    # Optionally, delete related registrations
    await db.registrations.delete_many({"event_id": event_id})
    
    return {"detail": "Event deleted successfully"}
