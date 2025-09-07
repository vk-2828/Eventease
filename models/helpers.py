def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "roles": user.get("roles", ["participant"])
    }

def event_helper(event) -> dict:
    return {
        "id": str(event["_id"]),
        "title": event["title"],
        "date": event["date"],
        "venue": event.get("venue", ""),
        "description": event.get("description", ""),
        "schedule": event.get("schedule", ""),
        "rules": event.get("rules", ""),
        "contact": event.get("contact", "")
    }

def registration_helper(reg) -> dict:
    return {
        "id": str(reg["_id"]),
        "event_id": reg["event_id"],
        "name": reg["name"],
        "email": reg["email"],
        "college": reg.get("college", ""),
        "phone": reg.get("phone", ""),
        "created_at": reg["created_at"]
    }
