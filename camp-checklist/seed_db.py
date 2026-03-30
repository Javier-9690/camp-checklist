"""Seed the database with rooms. Run once on deployment."""
import os
from app import app
from models import db, Room
from rooms_data import get_all_rooms


def seed():
    with app.app_context():
        db.create_all()
        # Only seed if rooms table is empty
        if Room.query.first() is None:
            rooms = get_all_rooms()
            for code, building in rooms:
                db.session.add(Room(code=code, building=building))
            db.session.commit()
            print(f"Seeded {len(rooms)} rooms.")
        else:
            print("Rooms already seeded.")


if __name__ == '__main__':
    seed()
