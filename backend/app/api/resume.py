import os

from fastapi import APIRouter, UploadFile, File

from app.services.pdf_parser import extract_text_from_pdf
from app.services.resume_parser import parse_resume

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)

    parsed = parse_resume(text)

    return {
        "filename": file.filename,
        "resume": parsed,
        "resume_text": text
    }