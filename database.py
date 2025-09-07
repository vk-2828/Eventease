from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Optional: create indexes
async def ensure_indexes():
    await db.events.create_index([("title", "text"), ("description", "text"), ("rules", "text")])
