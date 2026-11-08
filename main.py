from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Any

app = FastAPI(
    title="Akwaaba Store Mock API",
    description="Synthetic inventory, order, and delivery data for testing Kasa HTTP tools.",
    version="1.0.0",
)

# CORS is not required for Kasa's server-side HTTP tool calls, but makes
# the mock API convenient to inspect from browser-based test clients.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

PRODUCTS: dict[str, dict[str, Any]] = {
    "PHN-001": {
        "product_id": "PHN-001",
        "name": "Samsung Galaxy A16",
        "quantity": 12,
        "in_stock": True,
        "unit": "piece",
    },
    "PHN-002": {
        "product_id": "PHN-002",
        "name": "Redmi Note 14",
        "quantity": 0,
        "in_stock": False,
        "unit": "piece",
    },
    "PHN-003": {
        "product_id": "PHN-003",
        "name": "iPhone 13 (128GB)",
        "quantity": 5,
        "in_stock": True,
        "unit": "piece",
    },
    "LAP-001": {
        "product_id": "LAP-001",
        "name": "HP 250 G10",
        "quantity": 8,
        "in_stock": True,
        "unit": "piece",
    },
    "LAP-002": {
        "product_id": "LAP-002",
        "name": "Lenovo IdeaPad Slim 3",
        "quantity": 3,
        "in_stock": True,
        "unit": "piece",
    },
}

ORDERS: dict[str, dict[str, Any]] = {
    "AKW-1001": {
        "order_id": "AKW-1001",
        "status": "shipped",
        "payment_status": "paid",
        "items": [
            {"product_id": "PHN-001", "name": "Samsung Galaxy A16", "quantity": 1}
        ],
        "total": 1650.00,
        "currency": "GHS",
        "destination": "Accra Central",
        "estimated_delivery": "1-2 business days",
        "tracking_reference": "AKW-TRK-1001",
    },
    "AKW-1002": {
        "order_id": "AKW-1002",
        "status": "processing",
        "payment_status": "paid",
        "items": [
            {"product_id": "LAP-001", "name": "HP 250 G10", "quantity": 1}
        ],
        "total": 6500.00,
        "currency": "GHS",
        "destination": "Tema",
        "estimated_delivery": "1-3 business days after dispatch",
        "tracking_reference": None,
    },
    "AKW-1003": {
        "order_id": "AKW-1003",
        "status": "delivered",
        "payment_status": "paid",
        "items": [
            {"product_id": "ACC-001", "name": "Oraimo FreePods 4", "quantity": 2}
        ],
        "total": 900.00,
        "currency": "GHS",
        "destination": "Greater Accra",
        "estimated_delivery": "Delivered",
        "tracking_reference": "AKW-TRK-1003",
    },
}

# Fictional fees for testing only. These are not real Akwaaba Store rates.
DELIVERY_RATES = {
    "accra central": {"fee": 25.00, "estimate": "1-2 business days"},
    "greater accra": {"fee": 35.00, "estimate": "1-3 business days"},
    "tema": {"fee": 40.00, "estimate": "1-3 business days"},
    "kumasi": {"fee": 65.00, "estimate": "2-5 business days"},
    "takoradi": {"fee": 70.00, "estimate": "2-5 business days"},
}

@app.get("/")
def root():
    return {
        "service": "Akwaaba Store Mock API",
        "version": "1.0.0",
        "status": "ok",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/products/{product_id}/stock")
def check_product_stock(product_id: str):
    product = PRODUCTS.get(product_id.upper())
    if product is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "PRODUCT_NOT_FOUND",
                "message": f"No product was found with ID {product_id}.",
                "product_id": product_id,
            },
        )

    return {
        **product,
        "availability": "in_stock" if product["in_stock"] else "out_of_stock",
        "message": (
            f"{product['name']} is currently in stock."
            if product["in_stock"]
            else f"{product['name']} is currently out of stock."
        ),
    }

@app.get("/orders/{order_id}")
def get_order_status(order_id: str):
    order = ORDERS.get(order_id.upper())
    if order is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "ORDER_NOT_FOUND",
                "message": f"No order was found with reference {order_id}.",
                "order_id": order_id,
            },
        )
    return order

@app.get("/delivery/fee")
def calculate_delivery_fee(
    destination: str = Query(..., min_length=2, description="Delivery area or city")
):
    key = " ".join(destination.strip().lower().split())
    rate = DELIVERY_RATES.get(key)

    if rate is None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "DESTINATION_NOT_SUPPORTED",
                "message": (
                    f"We could not calculate a delivery fee for '{destination}'. "
                    "Please contact customer support to confirm service availability."
                ),
                "destination": destination,
                "supported_destinations": [
                    "Accra Central", "Greater Accra", "Tema", "Kumasi", "Takoradi"
                ],
            },
        )

    return {
        "destination": destination.strip(),
        "serviceable": True,
        "delivery_fee": rate["fee"],
        "currency": "GHS",
        "estimated_delivery": rate["estimate"],
        "note": "This is synthetic test data, not a real delivery quote.",
    }
