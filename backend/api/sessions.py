from fastapi import APIRouter, Depends, HTTPException
import os
import json
from typing import List
from ..auth.utils import get_current_user
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlmodel import Session as DBSession, select
from ..auth.utils import get_current_user
from ..database.models import UserSession, get_session
load_dotenv()

fernet_key = os.getenv("FERNET_KEY")
if not fernet_key:
    raise ValueError("FERNET_KEY not found in environment")

cipher = Fernet("cNOn_dJHOYu_JbniaDv0eMV55otIKvlkUqwQ4zslJMI=".encode())

router = APIRouter()

class MessageItem(BaseModel):
    sender: str
    text: str

class SessionItem(BaseModel):
    id: str
    title: str

class SessionMessagesResponse(BaseModel):
    session_id: str
    messages: List[MessageItem]


# get the user directory based on user id
def get_user_dir(user_id: str):
    return f"ashaaiflow/src/ashaaiflow/knowledge/{user_id}"


@router.get("/sessions", response_model=List[str])
def list_sessions(
    current_user = Depends(get_current_user),
    db: DBSession    = Depends(get_session)
):
    """
    Return all session IDs for the logged-in user.
    """
    sessions = db.exec(
        select(UserSession).where(UserSession.user_id == current_user.id)
    ).all()
    
    return [s.id for s in sessions]

# Route to get all messages from a session (decrypted)
@router.get("/session/{session_id}/messages", response_model=SessionMessagesResponse)
def get_session_messages(session_id: str, current_user=Depends(get_current_user)):
    user_dir = get_user_dir(current_user.id)
    session_dir = os.path.join(user_dir, session_id)
    
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found")
    
    conversation_path = os.path.join(session_dir, "conversation.json")
    
    if not os.path.exists(conversation_path):
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    with open(conversation_path) as f:
        hist = json.load(f)
    
    decrypted_messages = []
    for m in hist:
        try:
            raw_text = str(m.get("text", ""))
            txt = cipher.decrypt(raw_text.encode("utf-8")).decode("utf-8")
        except:
            txt = ""  
        decrypted_messages.append(MessageItem(sender=m["sender"], text=txt))
    
    return SessionMessagesResponse(session_id=session_id, messages=decrypted_messages)


# Utility function to save message to conversation.json (encrypting text before saving)
def save_message_to_conversation(session_id: str, user_text: str, ai_text: str, user_id: str):
    session_dir = os.path.join(get_user_dir(user_id), session_id)
    
    os.makedirs(session_dir, exist_ok=True)
    
    conversation_path = os.path.join(session_dir, "conversation.json")
    
    if not os.path.exists(conversation_path):
        with open(conversation_path, "w") as f:
            json.dump([], f)  
    
    enc_user = cipher.encrypt(user_text.encode()).decode()
    enc_bot = cipher.encrypt(ai_text.encode()).decode()
    
    with open(conversation_path, "r+") as f:
        history = json.load(f)
        history.append({"sender": "user", "text": enc_user})
        history.append({"sender": "bot", "text": enc_bot})
        f.seek(0)
        json.dump(history, f, indent=2)
        f.truncate()
