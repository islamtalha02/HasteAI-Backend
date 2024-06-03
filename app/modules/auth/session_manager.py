# backend/session_manager.py
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models.session_model import Session as SessionModel
from sqlalchemy.orm import Query

def create_session(db: Session, user_id: str, duration: int = 30):
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=duration)
    session_data = SessionModel(
        session_id=session_id,
        data=user_id,
        expires_at=expires_at,
    )
    db.add(session_data)
    db.commit()
    db.refresh(session_data)
    return session_data

def get_session(db: Session, session_id: str):
    return db.query(SessionModel).filter(
        SessionModel.session_id == session_id, 
        SessionModel.is_active == True,
        SessionModel.expires_at > datetime.utcnow()
    ).first()

def delete_session(db: Session, session_id: str):
    session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if session:
        session.is_active = False # type: ignore

        db.commit()
        return True
    return False
