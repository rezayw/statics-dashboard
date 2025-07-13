# statics-dashboard

Web static-dashboard app for uploading and fetch images, lightweight, using django uvicorn

## Features
- Auto convert to webp for image exension
- Authorization fetch cosume
- Image listing and Preview
- Authentication

## RUNNING PROGRAM

```bash
python -m venv venv
source venv/bin/activate  # for macOS/Linux
venv\Scripts\activate     # for Windows
```

## RUNNING API

```bash
uvicorn app.main:app --reload
```

## CHECK API DOCS (SWAGGER)

```bash

http://127.0.0.1:8000/docs

```

## LOGIN & REGISTER API
```bash
# Register
POST /api/register
```bash

#JSON PAYLOAD
{
  "email": "admin@example.com",
  "full_name": "Admin User",
  "password": "yourpassword"
}
```

```bash
#Login
POST /api/login

#JSON PAYLOAD
{
  "email": "admin@example.com",
  "password": "yourpassword"
}
```

# CONSUME
```bash
const API_URL = "http://127.0.0.1:8000/api/files";
const TOKEN = "YOUR_TOKEN_HERE";
```
