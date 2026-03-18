from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.user_service import create_user, authenticate_user
from app.services.jwt_service import ALGORITHM, SECRET_KEY, create_access_token, create_refresh_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.name, user.email, user.password)
    return {"message": "User created", "user_id": new_user.id}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        email = payload.get("sub")

        new_access_token = create_access_token({"sub": email})

        return {"access_token": new_access_token}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")