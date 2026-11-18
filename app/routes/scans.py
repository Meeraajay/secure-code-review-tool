
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.services.git_service import validate_github_url

router = APIRouter(prefix="/scans", tags=["Scans"])


class ScanRequest(BaseModel):
    repository_url: HttpUrl


@router.post("/")
def create_scan(request: ScanRequest):

    repository_url = str(request.repository_url)

    if not validate_github_url(repository_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )

    return {
        "message": "GitHub repository URL validated successfully",
        "repository_url": repository_url
    }
