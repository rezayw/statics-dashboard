from fastapi import APIRouter, Request, UploadFile, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import File as FastAPIFile  # ⛔ Hindari konflik nama dengan model File
from app.auth.jwt_handler import get_current_user
from app.crud.file import save_file_record, list_file_records
from app.db.base import SessionLocal
from app.models.file import File

import shutil, os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user=Depends(get_current_user)):
    files = list_file_records()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "user": user,
        "files": files
    })

@router.post("/upload-form")
def upload_from_ui(
    request: Request,
    file: UploadFile = FastAPIFile(...),  # ✅ gunakan alias
    user=Depends(get_current_user)
):
    ext = file.filename.split(".")[-1].lower()
    folder_map = {"jpg": "images", "png": "images", "mp4": "videos", "pdf": "pdfs", "txt": "texts"}
    folder = folder_map.get(ext, "others")

    save_path = f"static/{folder}/{file.filename}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    save_file_record(file.filename, folder, save_path)
    return RedirectResponse(url="/api/dashboard", status_code=302)

@router.post("/delete-file")
def delete_file(filename: str = Form(...), user=Depends(get_current_user)):
    db = SessionLocal()
    file_record = db.query(File).filter(File.filename == filename).first()

    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # hapus file dari file system
    if os.path.exists(file_record.path):
        os.remove(file_record.path)

    # hapus dari database
    db.delete(file_record)
    db.commit()
    db.close()

    return RedirectResponse(url="/api/dashboard", status_code=303)
