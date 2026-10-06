import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.disease_scan import DiseaseScan


router = APIRouter()


@router.post("/scan")
async def create_scan(
    field_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    extension = os.path.splitext(
        image.filename or ""
    )[1].lower()

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format"
        )

    os.makedirs(
        os.path.join(
            settings.UPLOAD_DIR,
            "plant_health"
        ),
        exist_ok=True
    )

    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        "plant_health",
        filename
    )

    content = await image.read()

    with open(file_path, "wb") as file:
        file.write(content)

    scan = DiseaseScan(
        field_id=field_id,
        image_path=file_path,
        status="pending"
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return {
        "success": True,
        "scan_id": scan.id,
        "status": "pending",
        "message": "Image uploaded. AI analysis will be integrated."
    }


@router.get("/{scan_id}")
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db)
):
    scan = db.query(DiseaseScan).filter(
        DiseaseScan.id == scan_id
    ).first()

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Scan not found"
        )

    return scan