from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from ashaaiflow.src.ashaaiflow.main import CareerGuidanceFlow
from ashaaiflow.src.ashaaiflow.crews.resume_crew.resume_crew import ResumeCrew
import os
from fastapi.security import HTTPBearer
from shared.user_context import user_id_var,session_id_var
from cryptography.fernet import Fernet
from .sessions import save_message_to_conversation
import json
from dotenv import load_dotenv
from sqlmodel import Session as DBSession
from ..auth.utils import get_current_user, create_or_get_session
from fastapi import Form
from typing import Optional
from ..database.models import get_session
load_dotenv() 

BASE_KNOWLEDGE_DIR = "ashaaiflow/src/ashaaiflow/knowledge"

router = APIRouter()
http_bearer = HTTPBearer()

fernet_key = os.getenv("FERNET_KEY").encode()
cipher = Fernet(fernet_key)

class UserQueryRequest(BaseModel):
    user_query: str
    session_id: str = None


@router.post("/run-flow")
def run_flow(
    payload: UserQueryRequest, 
    current_user=Depends(get_current_user),
    db: DBSession=Depends(get_session),
):
    
    try:        
        user_name = current_user.name
        print(payload.session_id)
        session_id = payload.session_id or  create_or_get_session(current_user.id, db)
        session_dir = os.path.join(BASE_KNOWLEDGE_DIR, str(current_user.id), session_id)
        os.makedirs(session_dir, exist_ok=True)
        conversation_path = os.path.join(session_dir, "conversation.json")

        if not os.path.exists(conversation_path):
            with open(conversation_path, "w") as f:
                json.dump([], f)

        user_id_var.set(current_user.id)
        session_id_var.set(session_id)
        content_flow = CareerGuidanceFlow()
        content_flow.state.user_query = payload.user_query
        content_flow.state.user_id = current_user.id
        content_flow.state.session_id = session_id
        content_flow.state.user_name = user_name
        
        result = content_flow.kickoff()
        
        user_text = content_flow.state.user_query
        ai_text = content_flow.state.response
        
        save_message_to_conversation(
            session_id=session_id,
            user_text=user_text,
            ai_text=ai_text,
            user_id=str(current_user.id)
        )
        
        print(content_flow.state.response)
        
        return {"result": content_flow.state.response , "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ResumeUploadRequest(BaseModel):
    session_id: str = None
    
    
@router.post("/upload-resume")
def upload_and_analyze_resume(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: DBSession = Depends(get_session),
    session_id: Optional[str] = Form(None)
):
    if not file.filename.endswith((".pdf", ".docx", ".doc")):
        raise HTTPException(status_code=400, detail="Only .pdf, .docx, or .txt files allowed.")

    session_id = session_id or create_or_get_session(current_user.id, db)
    session_dir = os.path.join(BASE_KNOWLEDGE_DIR, str(current_user.id), session_id)
    os.makedirs(session_dir, exist_ok=True)

    # 3️⃣ Clean out old resume files in *this* session
    for existing in os.listdir(session_dir):
        path = os.path.join(session_dir, existing)
        if os.path.isfile(path) and existing.lower().endswith((".pdf", ".docx", ".doc")):
            os.remove(path)

    resume_path = os.path.join(session_dir, file.filename)

    try:
        with open(resume_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        user_id_var.set(current_user.id)
        session_id_var.set(session_id)
        resume_crew = ResumeCrew()
        result = resume_crew.crew().kickoff()
        
        user_text = "Resume Uploaded" 
        ai_text = result.raw
        
        save_message_to_conversation(
            session_id=session_id,
            user_text=user_text,
            ai_text=ai_text,
            user_id=str(current_user.id)
        )
    
        return {"result": result.raw,"session_id": session_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {e}")
