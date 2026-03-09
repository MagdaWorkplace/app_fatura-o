from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from security import get_current_user
from models import Invoice
from qr_reading import read_qr
from qr_parsing import parse_qr
from qr_validator import validate_qr
router = APIRouter()

@router.post("/upload-invoice")
def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Read image bytes.
    image_bytes = file.file.read()

    # Decode QR
    qr_data = read_qr(image_bytes)

    if not qr_data:
        raise HTTPException(status_code=400, detail="QR code not found")

    # Parse the QR data.
    invoice_information = parse_qr(qr_data)

    # Validate the data.
    validated_data = validate_qr(invoice_information)

    # Save the information into the db.
    new_invoice = Invoice(
        user_id = current_user.id,
        seller_name = validated_data["seller_name"],
        seller_nif = validated_data["seller_nif"],
        invoice_date = validated_data["invoice_date"],
        total_amount = validated_data["total_amount"],
        qr_raw_data = qr_data
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return {"message": "Invoice update successfully",
            "QR data": qr_data
            }
