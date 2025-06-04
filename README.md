# PROJECT STRUCTURE

project/
├── app/
│   ├── main.py
│   ├── core/config.py
│   ├── auth/jwt_handler.py
│   ├── db/base.py
│   ├── models/file.py
│   ├── crud/file.py
│   ├── routes/upload.py
│   └── templates/admin.html
├── static/
│   ├── images/
│   ├── videos/
│   ├── pdfs/
│   └── texts/
├── requirements.txt
└── .env

# RUNNING PROGRAM

python -m venv venv
source venv/bin/activate  # untuk macOS/Linux
venv\Scripts\activate     # untuk Windows

# RUNNING API

uvicorn app.main:app --reload

# CHECK API DOCS (SWAGGER)

http://127.0.0.1:8000/docs


