import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session
from ..database.models import get_session
from ..auth.utils import get_current_user

# CrewAI logic
from ...ashaaiflow.src.ashaaiflow.main import CareerGuidanceFlow
from ...ashaaiflow.src.ashaaiflow.crews.resume_crew.resume_crew import ResumeCrew

router = APIRouter()

# Request body expects only user_query
class UserQueryRequest(BaseModel):
    user_query: str

@router.post("/run-flow", status_code=status.HTTP_200_OK)
def run_flow(
    payload: UserQueryRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    try:
        content_flow = CareerGuidanceFlow()
        content_flow.state.user_id = current_user.id
        content_flow.state.user_query = payload.user_query
        result = content_flow.kickoff()
        return {"result": content_flow.state.response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-resume", status_code=status.HTTP_200_OK)
def upload_and_analyze_resume(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    # Validate file type
    if not file.filename.endswith((".pdf", ".docx", ".doc")):
        raise HTTPException(status_code=400, detail="Only .pdf, .docx, or .txt files allowed.")

    UPLOAD_DIR = f"../../../ashaaiflow/src/ashaaiflow/knowledge/{current_user.id}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Ensure unique filename
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        agent = ResumeAgent()
        analysis = agent.run(file_path, user_id=current_user.id)
        return {
            "message": "Resume analyzed successfully.",
            "filename": file.filename,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {e}")
