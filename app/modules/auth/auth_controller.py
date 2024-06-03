# backend/auth_controller.py
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .schema.register_schema import UserRegistration
from .schema.login_schema import UserLogin
from .models.user_model import User
from ...db.database import get_db
from .session_manager import create_session, get_session, delete_session

router = APIRouter()

SECRET = "your-secret-key"



@router.post('/login')
async def login(data: UserLogin, db: Session = Depends(get_db)):
    user_role = data.user_role
    password = data.password
    # Perform your user authentication here
    if user_role == "admin" and password == "admin":  # Simplified check
        session = create_session(db, user_role)
        response = {
            "message": "Logged in",
            "session_id": session.session_id
        }
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get('/logout')
async def logout(session_id: str = Cookie(None), db: Session = Depends(get_db)):
    if not session_id:
        raise HTTPException(status_code=400, detail="No session cookie found")
    success = delete_session(db, session_id)
    if success:
        return {"message": "Logged out"}
    else:
        raise HTTPException(status_code=400, detail="Invalid session")

@router.get('/session')
async def get_current_session(session_id: str = Cookie(None), db: Session = Depends(get_db)): # type: ignore
    if not session_id:
        raise HTTPException(status_code=400, detail="No session cookie found")
    session = get_session(db, session_id)
    if session:
        return {"user": session.data}
    else:
        raise HTTPException(status_code=401, detail="Not authenticated")
@router.post('/signup')
async def signup(data: UserRegistration, db: Session = Depends(get_db)):
    # Check if user already exists
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    new_user = User(username=data.username, email=data.email, password=data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create session
    session = create_session(db, new_user.username) # type: ignore

    response = {
        "message": "User created successfully",
        "session_id": session.session_id
    }
    return response