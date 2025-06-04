from app.db.base import SessionLocal
from app.models.file import File

def save_file_record(filename, filetype, path):
    db = SessionLocal()
    record = File(filename=filename, filetype=filetype, path=path)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": "Uploaded", "id": record.id}

def list_file_records():
    db = SessionLocal()
    return db.query(File).all()

def list_by_type(filetype: str):
    db = SessionLocal()
    return db.query(File).filter(File.filetype == filetype).all()

def delete_file(file_id: int):
    db = SessionLocal()
    obj = db.query(File).filter(File.id == file_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False