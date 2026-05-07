from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password


def seed_data(db: Session):
    # controlla se esiste già admin
    existing_user = db.query(User).filter(User.email == "admin@test.com").first()

    if existing_user:
        print("Admin già esistente")
        return

    admin = User(
        email="admin@test.com",
        full_name="Admin User",
        hashed_password=hash_password("admin123"),
        is_active=True,
        is_verified=True,
    )

    db.add(admin)
    db.commit()

    print("Admin creato: admin@test.com / admin123")