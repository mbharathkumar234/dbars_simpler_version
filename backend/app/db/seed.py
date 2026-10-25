"""
Quick script to populate the database with some dummy Bengaluru commuter data.
This lets us test the UI without having to manually click through the app 100 times.
Run it via: python -m app.db.seed
"""
from __future__ import annotations

import asyncio
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ensure the backend directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.auth.auth import hash_password
from app.db.database import get_db, init_db

async def seed() -> None:
    """Wipe or populate the DB with initial demo data."""
    await init_db()
    print("[DB] Database initialized.")

    async for db in get_db():
        # let's grab the total number of users first to see if we already ran this script
        existing_count = await db.users.count_documents({})
        if existing_count > 10:
            print(f"[WARN] Looks like the DB already has {existing_count} users. Bailing out so we don't duplicate stuff.")
            return

        # ── Create admin & depot users manually if they don't exist ──
        if not await db.users.find_one({"email": "admin@bmtc.gov.in"}):
            await db.users.insert_one({
                "email": "admin@bmtc.gov.in",
                "name": "Admin",
                "password_hash": hash_password("admin123"),
                "role": "admin",
                "preferred_lang": "en",
                "reliability": 1.0,
                "is_active": 1,
                "created_at": datetime.now(timezone.utc)
            })

        if not await db.users.find_one({"email": "depot@bmtc.gov.in"}):
            await db.users.insert_one({
                "email": "depot@bmtc.gov.in",
                "name": "Depot Manager",
                "password_hash": hash_password("depot123"),
                "role": "depot_manager",
                "preferred_lang": "en",
                "reliability": 1.0,
                "is_active": 1,
                "created_at": datetime.now(timezone.utc)
            })

        print("[SEED] Default admin and depot manager accounts ensured.")

    print("\n[DONE] Database initialization complete!")
    print("   Default accounts:")
    print("   Admin:    admin@bmtc.gov.in / admin123")
    print("   Depot:    depot@bmtc.gov.in / depot123")


if __name__ == "__main__":
    asyncio.run(seed())
