# from fastapi import APIRouter, Depends, HTTPException
# from database import db
# from models.helpers import event_helper
# from schemas.event import EventCreate, EventOut
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from config import JWT_SECRET, JWT_ALGORITHM

# router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# @router.post("/", response_model=EventOut)
# async def create_event(event: EventCreate, token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         roles = payload.get("roles", [])
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     if "organizer" not in roles:
#         raise HTTPException(status_code=403, detail="Only organizers can create events")

#     result = await db.events.insert_one(event.dict())
#     return event_helper(await db.events.find_one({"_id": result.inserted_id}))

# @router.get("/", response_model=list[EventOut])
# async def list_events():
#     events = []
#     async for event in db.events.find():
#         events.append(event_helper(event))
#     return events
from fastapi import APIRouter, Depends, HTTPException
from database import db
from models.helpers import event_helper
from schemas.event import EventCreate, EventOut
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import JWT_SECRET, JWT_ALGORITHM

router = APIRouter()

# Fix the tokenUrl to be relative to the user router's prefix
# Assuming the user router is mounted with a prefix like `router.include_router(user_router, prefix="/users")`
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/", response_model=EventOut)
async def create_event(event: EventCreate, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        roles = payload.get("roles", [])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if "organizer" not in roles:
        raise HTTPException(status_code=403, detail="Only organizers can create events")

    result = await db.events.insert_one(event.dict())
    return event_helper(await db.events.find_one({"_id": result.inserted_id}))

@router.get("/", response_model=list[EventOut])
async def list_events():
    events = []
    async for event in db.events.find():
        events.append(event_helper(event))
    return events