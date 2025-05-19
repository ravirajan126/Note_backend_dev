from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.user.models import User
from app.security import create_access_token
from passlib.hash import bcrypt


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", tags=["User"])
async def register(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user_name = data.get("user_name")
    user_email = data.get("user_email")
    password = data.get("password")

    if not all([user_name, user_email, password]):
        raise HTTPException(status_code=400, detail="Missing fields")

    db_user = db.query(User).filter(User.user_email == user_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = bcrypt.hash(password)
    new_user = User(user_email=user_email, user_name=user_name, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"sub": new_user.user_email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/signin", tags=["User"])
async def signin(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    user_email = data.get("user_email")
    password = data.get("password")

    if not all([user_email, password]):
        raise HTTPException(status_code=400, detail="Missing email or password")

    user = db.query(User).filter(User.user_email == user_email).first()
    if not user or not bcrypt.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.user_email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "user_name": user.user_name,
        "user_email": user.user_email
    }
