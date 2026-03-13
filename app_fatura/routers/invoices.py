from fastapi import  APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db import get_db
from security import get_current_user
from models import Invoice

router = APIRouter()

@router.get("/invoices")
def get_user_invoices(
    # Filters.
    seller_name: str = Query(None, description="Filter the invoices by the seller name"),
    total_amount: float = Query(None, description="Filter the invoices by amount"),
    invoice_date: float = Query(None, description="Filter the invoices by date YYYY-MM-DD"),

    # Database session and current user.
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only get the current user invoices.
    query = db.query(Invoice).filter(Invoice.user_id == current_user.id)

    # If information provided:
        # Filter by seller name.
    if seller_name:
        query = query.filter(Invoice.seller_name.ilike(f"%{seller_name}%"))

        # Filter by amount.
        if total_amount:
            query = query.filter(Invoice.total_amount == total_amount)

        # Filter by specific invoice date.
        if invoice_date:
            try:
                # Convert the string (date) into datetime object.
                date_object = datetime.strftime(invoice_date, "%Y-%m-%d")

                # Filter the invoice matching that date.
                query = query.filter(Invoice.invoice_date == date_object)

            except ValueError:
                # if the formate is wrong, give an error.
                return {"Error! Date must be YYYY-MM-DD format"}

        # Execute the request/query.
        invoices = query.all()

        # Convert database objects to JSON format.
        result = []

        for invoice in invoices:
            result.append({
                "id": invoice.id,
                "seller_name": invoice.seller_name,
                "seller_nif": invoice.seller_nif,
                "invoice_date": invoice.invoice_date,
                "total_amount": invoice.total_amount
            })

    # Return the invoices and how mny where found.
    return {
        "invoices": result,
        "count": len(result)

    }
