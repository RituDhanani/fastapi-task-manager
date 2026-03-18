from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth_services import hash_password, verify_password

def create_user(db: Session, name: str, email: str, password: str, role: str = "user"):
    hashed_password = hash_password(password)

    user = User(
        name=name,
        email=email,
        password=hashed_password,
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user