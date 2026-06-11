import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, User, Base, engine
from routers.auth import hash_password

def seed_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin_email = "admin"
        existing = db.query(User).filter(User.email == admin_email).first()
        if existing:
            # ensure role is admin
            existing.role = "admin"
            db.commit()
            print("Admin account already exists and verified.")
            return

        new_admin = User(
            name="Administrator",
            email=admin_email,
            password_hash=hash_password("admin"),
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        print("Admin account 'admin' created successfully with password 'admin'.")
    except Exception as e:
        print("Error seeding admin:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
