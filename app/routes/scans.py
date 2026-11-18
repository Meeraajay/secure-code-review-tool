from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.services.git_service import (
    validate_github_url,
    clone_repository,
    find_python_files
)

from app.services.scanner_service import run_all_scanners


router = APIRouter(prefix="/scans", tags=["Scans"])


class ScanRequest(BaseModel):
    repository_url: HttpUrl


@router.post("/")
def create_scan(request: ScanRequest):

    repository_url = str(request.repository_url)

    # Step 1: Validate the GitHub URL
    if not validate_github_url(repository_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )

    try:
        # Step 2: Clone the repository
        repository_path = clone_repository(repository_url)

        # Step 3: Find Python files
        python_files = find_python_files(repository_path)

        if not python_files:
            raise HTTPException(
                status_code=400,
                detail="No Python files found in this repository"
            )

        # Step 4: Run Bandit and Semgrep
        scan_results = run_all_scanners(repository_path, python_files)

        return {
            "message": "Repository scanned successfully",
            "repository_url": repository_url,
            "python_file_count": len(python_files),
            "reports": scan_results["reports"]
        }

    except FileExistsError:
        raise HTTPException(
            status_code=409,
            detail="Repository already exists locally. Remove the existing clone before scanning again."
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )