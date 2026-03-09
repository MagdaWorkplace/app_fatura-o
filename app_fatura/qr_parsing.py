from urllib.parse import urlparse, parse_qs

def parse_qr (qr_data: str):

    # Extract the information from the invoice QR code.
    parse = urlparse(qr_data)
    query = parse_qs(parse.query)

    return {
        "seller_name" : query.get("emitente", [""])[0],
        "seller_nif": query.get("nif", [""])[0],
        "total_amount": query.get("total", [""])[0],
        "invoice_date": query.get("data", [""])[0],

    }