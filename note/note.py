from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.note.models import Note
from app.user.models import User
from app.database import SessionLocal
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/notes/create", tags=["Notes"])
async def create_note(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    note_title = data.get("note_title")
    note_content = data.get("note_content")
    user_id = data.get("user_id")

    if not all([note_title, note_content, user_id]):
        return {"error": "Missing fields"}

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_note = Note(note_id=str(uuid.uuid4()), note_title=note_title, note_content=note_content, user_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/notes/{user_id}", tags=["Notes"])
def get_notes_by_user(user_id: str, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    return notes

@router.put("/notes/{note_id}", tags=["Notes"])
async def update_note(note_id: str, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.note_title = data.get("note_title", note.note_title)
    note.note_content = data.get("note_content", note.note_content)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/notes/{note_id}", tags=["Notes"])
def delete_note(note_id: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}
