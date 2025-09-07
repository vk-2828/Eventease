from fastapi import FastAPI
from routes import users, events, registrations, auth_routes, ai_agent

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Welcome to EventEase API 🚀"}

# Register routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(registrations.router, prefix="/registrations", tags=["Registrations"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(ai_agent.router, prefix="/ai", tags=["AI Agent"])
