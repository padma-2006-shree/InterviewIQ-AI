import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_parser import extract_text_from_file
from app.services.resume_parser import parse_resume

router = APIRouter(prefix="/resume", tags=["Resume"])

# On Vercel serverless environments, use /tmp which is the only writable directory
if os.getenv("VERCEL"):
    UPLOAD_FOLDER = Path("/tmp/uploads")
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    UPLOAD_FOLDER = BASE_DIR / "uploads"

try:
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    file_path = UPLOAD_FOLDER / file.filename

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        text = extract_text_from_file(str(file_path))

        if not text or text.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Could not extract readable text from the uploaded document. Please check the file."
            )

        parsed = parse_resume(text)

        return {
            "filename": file.filename,
            "resume": parsed,
            "resume_text": text
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")
