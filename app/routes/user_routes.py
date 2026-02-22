from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import SessionLocal
from ..models import User
from ..schemas import UserCreate
from ..auth import hash_password, verify_password, create_access_token
from ..redis_client import r
from ..auth_dependency import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = hash_password(user.password)

    new_user = User(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):

    r.setex(f"blacklist:{token}", 7200, "true")

    return {"message": "Logged out successfully"}