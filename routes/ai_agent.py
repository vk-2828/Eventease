from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from database import db
import google.generativeai as genai
import os
from jose import jwt

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

# JWT auth
async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

class AIRequest(BaseModel):
    question: str
    max_output_tokens: int = 300

@router.post("/ask")
async def ask_ai(request: AIRequest, current_user: dict = Depends(get_current_user)):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    # Organizer-only description
    if "description" in question.lower():
        if "organizer" not in current_user.get("roles", []):
            raise HTTPException(status_code=403, detail="Only organizers can generate descriptions")
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Generate event description for:\n{question}")
            return {"answer": response.text}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Otherwise search DB
    events = []
    async for event in db.events.find():
        events.append(event)

    if not events:
        return {"answer": "No events found"}

    keywords = question.lower().split()
    matching_events = [e for e in events if any(kw in e.get("title", "").lower() for kw in keywords)]

    if not matching_events:
        return {"answer": "No matching events found"}

    event_context = ""
    for e in matching_events:
        event_context += (
            f"Title: {e.get('title')}\n"
            f"Date: {e.get('date')}\n"
            f"Venue: {e.get('venue')}\n"
            f"Schedule: {e.get('schedule')}\n"
            f"Rules: {e.get('rules')}\n"
            f"Contact: {e.get('contact')}\n\n"
        )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Here are matching events:\n{event_context}\nQuestion: {question}")
        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))