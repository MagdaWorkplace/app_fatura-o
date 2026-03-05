from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from security import get_current_user
from models import Invoice
from qr_reading import read_qr

router = APIRouter()

@router.post("/upload-invoice")
def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Read image bytes.
    image_bytes = file.file.read()

    # Decode QR
    qr_data = read_qr(image_bytes)

    if not qr_data:
        raise HTTPException(status_code=400, detail="QR code not found")

    # Save the information into the db,
    new_invoice = Invoice(user_id = current_user.id, qr_reading = qr_data)

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return {"message": "Invoice update successfully",
            "QR data": qr_data
            }
