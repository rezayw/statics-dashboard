from fastapi import APIRouter, UploadFile, File, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth.jwt_handler import get_current_user
from app.crud.file import save_file_record, list_file_records
import shutil, os
from fastapi import HTTPException

ALLOWED_EXTENSIONS = {"jpg", "png", "mp4", "pdf", "txt"}
MAX_FILE_SIZE_MB = 10

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@router.post("/upload")
def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    ext = file.filename.split(".")[-1].lower()

    # Validasi ekstensi
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed.")

    # Validasi ukuran (dalam byte)
    contents = file.file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=413, detail=f"File too large (> {MAX_FILE_SIZE_MB} MB)")

    # Reset cursor file
    file.file.seek(0)

    folder_map = {"jpg": "images", "png": "images", "mp4": "videos", "pdf": "pdfs", "txt": "texts"}
    folder = folder_map.get(ext, "others")
    save_path = f"static/{folder}/{file.filename}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return save_file_record(file.filename, folder, save_path)

@router.get("/files")
def get_files(user=Depends(get_current_user)):
    return list_file_records()