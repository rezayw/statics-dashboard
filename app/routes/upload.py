from fastapi import APIRouter, UploadFile, File, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth.jwt_handler import get_current_user
from app.crud.file import save_file_record, list_file_records
from PIL import Image
import shutil, os, io

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "mp4", "pdf", "txt"}
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

    # Validasi ukuran file
    contents = file.file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=413, detail=f"File too large (> {MAX_FILE_SIZE_MB} MB)")

    file.file.seek(0)  # Reset pointer

    folder_map = {"jpg": "images", "jpeg": "images", "png": "images", "mp4": "videos", "pdf": "pdfs", "txt": "texts"}
    folder = folder_map.get(ext, "others")
    os.makedirs(f"static/{folder}", exist_ok=True)

    # Kompresi Gambar ke WEBP
    if folder == "images":
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            webp_filename = file.filename.rsplit(".", 1)[0] + ".webp"
            save_path = f"static/{folder}/{webp_filename}"
            image.save(save_path, "WEBP", optimize=True, quality=80)
            return save_file_record(webp_filename, folder, save_path)
        except Exception:
            raise HTTPException(status_code=500, detail="Image compression failed")

    # File biasa (non-image)
    save_path = f"static/{folder}/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(io.BytesIO(contents), buffer)

    return save_file_record(file.filename, folder, save_path)

@router.get("/files")
def get_files(user=Depends(get_current_user)):
    return list_file_records()
