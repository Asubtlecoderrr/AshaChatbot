from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlmodel import Session, select
from ..database.models import get_session, User, get_db
from ..auth.utils import get_current_user, verify_access_token
from ashaaiflow.src.ashaaiflow.main import CareerGuidanceFlow
from ashaaiflow.src.ashaaiflow.crews.resume_crew.resume_crew import ResumeCrew
import os
import uuid
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from shared.user_context import user_id_var

router = APIRouter()
http_bearer = HTTPBearer()


# Request body expects only user_query
class UserQueryRequest(BaseModel):
    user_query: str

# Run flow - protected route requiring JWT token
@router.post("/run-flow")
def run_flow(
    payload: UserQueryRequest, 
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer), 
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    try:        
        
        user_name = db.exec(select(User.user_name).where(User.id == current_user.id)).first()
        
        path = f"ashaaiflow/src/ashaaiflow/knowledge/{current_user.id}/context.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        user_id_var.set(current_user.id)
        content_flow = CareerGuidanceFlow()
        content_flow.state.user_query = payload.user_query
        content_flow.state.user_id = current_user.id
        content_flow.state.user_name = user_name
            
        result = content_flow.kickoff()

        with open(path, "a+") as f:  # "a" mode = append
            f.write("User: "+ payload.user_query + "\n")
            f.write("AI: "+ content_flow.state.response + "\n")
        
        print(content_flow.state.response)
        
        return {"result": content_flow.state.response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-resume")
def upload_and_analyze_resume(file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Depends(http_bearer), current_user=Depends(get_current_user)):
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
        
        with open(path, "a+") as f:  # "a" mode = append
            f.write("User: Analyze the resume" + "\n")
            f.write("AI: "+ result.raw + "\n")
        return {"result": result.raw}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {e}")
