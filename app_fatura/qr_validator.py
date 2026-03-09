from datetime import datetime
from fastapi import HTTPException

def validate_qr (invoice_info: dict):
    # Validate NIF.
    nif = invoice_info.get("seller_nif")
    if not nif.isdigit() or len(nif) != 9:
        raise HTTPException(status_code=400, detail="Invalid seller NIF")

    # Validate total amount.
    try:
        total = float(invoice_info.get("total_amount"))

        if total < 0:
            raise ValueError()
    except ValueError:
        HTTPException(status_code=400, detail="Invalid amount")

    # Validate date formate.
    try:
        invoice_date = datetime.strftime(invoice_info.get("invoice_date"),"%Y-%m-%d")
    except ValueError:
        HTTPException(status_code=400, detail="Invalid date format")

    return {
        "seller_name": invoice_info.get("seller_name", ""),
        "seller_nif": nif,
        "total_amount": total,
        "invoice_date": invoice_date
    }