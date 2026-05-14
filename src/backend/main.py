"""
FastAPI server for Scientific Forgery Image Detection.

Endpoints:
- GET /         : health check
- POST /upload  : accepts an image, runs detection, returns result
"""

import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from detection import detect_copy_move

app = FastAPI(title="Scientific Forgery Image Detection API")

# Allow the frontend (running on a different port) to talk to this backend.
# In production you'd restrict allow_origins to your actual frontend URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder where uploaded images get saved temporarily.
UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    """Health check endpoint — visit this to confirm the server is running."""
    return {"status": "ok", "message": "Scientific Forgery Detection API"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Receive an uploaded image, run copy-move forgery detection, return result.
    """

    # 1. Validate the file is actually an image
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image (JPEG, PNG, etc.)"
        )

    # 2. Save the upload to disk with a unique filename
    #    (so two users uploading "test.jpg" at the same time don't collide)
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Run the detection logic, then clean up the temp file no matter what
    try:
        result = detect_copy_move(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return result
