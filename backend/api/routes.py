from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlmodel import Session, select
from ..auth.utils import get_current_user, verify_access_token
from ashaaiflow.src.ashaaiflow.main import CareerGuidanceFlow
from ashaaiflow.src.ashaaiflow.crews.resume_crew.resume_crew import ResumeCrew
import os
import uuid
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from shared.user_context import user_id_var
from cryptography.fernet import Fernet

from dotenv import load_dotenv
load_dotenv() 

router = APIRouter()
http_bearer = HTTPBearer()

fernet_key = os.getenv("FERNET_KEY").encode()
cipher = Fernet(fernet_key)

class UserQueryRequest(BaseModel):
    user_query: str

# Run flow - protected route requiring JWT token
@router.post("/run-flow")
def run_flow(
    payload: UserQueryRequest, 
    current_user=Depends(get_current_user)
):
    
    try:        
        user_name = current_user.name
        user_name = user_name.split(" ")[0] if user_name else user_name.split(" ")[1]
        path = f"ashaaiflow/src/ashaaiflow/knowledge/{current_user.id}/context.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("AI: " + """Hello! Welcome to ASHA AI 💜 You're in the perfect place to ask, learn, and grow — because YOU build tomorrow.  And it all starts with just one question !!""" + "\n")
            
        user_id_var.set(current_user.id)
        print(user_id_var.get(),"####################################################")
        content_flow = CareerGuidanceFlow()
        content_flow.state.user_query = payload.user_query
        content_flow.state.user_id = current_user.id
        content_flow.state.user_name = user_name
        
        result = content_flow.kickoff()
        user_text = "User: " + content_flow.state.user_query
        ai_text = "AI: " + content_flow.state.response
        encrypted_user = cipher.encrypt(user_text.encode()).decode()
        encrypted_ai = cipher.encrypt(ai_text.encode()).decode()
        
        with open(path, "a+") as f:  # "a" mode = append
            f.write(encrypted_user+ "\n")
            f.write(encrypted_ai + "\n")
        
        print(content_flow.state.response)
        
        return {"result": content_flow.state.response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-resume")
def upload_and_analyze_resume(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    if not file.filename.endswith((".pdf", ".docx", ".doc")):
        raise HTTPException(status_code=400, detail="Only .pdf, .docx, or .txt files allowed.")

    UPLOAD_DIR = f"ashaaiflow/src/ashaaiflow/knowledge/{current_user.id}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        path = f"ashaaiflow/src/ashaaiflow/knowledge/{current_user.id}/context.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        resume_crew = ResumeCrew()
        result = resume_crew.crew().kickoff()
        
        user_text = "User: Resume Uploaded" 
        ai_text = "AI: " + result.raw
        encrypted_user = cipher.encrypt(user_text.encode()).decode()
        encrypted_ai = cipher.encrypt(ai_text.encode()).decode()
        
        with open(path, "a+") as f:  # "a" mode = append
            f.write(encrypted_user+ "\n")
            f.write(encrypted_ai + "\n")
            
        return {"result": result.raw}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {e}")
