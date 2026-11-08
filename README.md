# Akwaaba Store Mock API

A small FastAPI service with synthetic inventory, order, and delivery data for testing Kasa HTTP tools.

> All inventory quantities, orders, delivery fees, and delivery estimates in this project are fictional test data. Do not use them to make real customer commitments.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the endpoints.

Kasa's hosted HTTP tool cannot call localhost/private-network addresses. Deploy this service to a public HTTPS host before connecting it to Kasa.

## Deploy on Render

1. Push this folder to a GitHub repository.
2. In Render, create a new **Blueprint** and select that repository.
3. Render reads `render.yaml` and creates the web service.
4. Wait for deployment to finish, then copy the public HTTPS service URL.
5. Test `https://YOUR-SERVICE.onrender.com/health` and `/docs`.

If you create the service manually instead of using the Blueprint:
- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

## Endpoints

### Check stock

`GET /products/{product_id}/stock`

Examples:
- `GET /products/PHN-001/stock` — Samsung Galaxy A16, 12 available
- `GET /products/PHN-002/stock` — Redmi Note 14, out of stock
- `GET /products/UNKNOWN/stock` — 404 product not found

### Get order

`GET /orders/{order_id}`

Examples:
- `GET /orders/AKW-1001` — shipped
- `GET /orders/AKW-1002` — processing
- `GET /orders/AKW-1003` — delivered
- `GET /orders/AKW-9999` — 404 order not found

### Calculate delivery fee

`GET /delivery/fee?destination=Accra%20Central`

Supported synthetic destinations:
- Accra Central: GH₵25
- Greater Accra: GH₵35
- Tema: GH₵40
- Kumasi: GH₵65
- Takoradi: GH₵70

An unsupported destination returns HTTP 400 with a structured error.

## Suggested Kasa HTTP tool configuration

Replace `https://YOUR-SERVICE.onrender.com` with the deployed service URL.

### 1. `check_product_stock`
- Method: `GET`
- URL: `https://YOUR-SERVICE.onrender.com/products/{product_id}/stock`
- Parameter: `product_id` (string, required)
- Description: Check the current stock quantity and availability for a product. Use the product ID from the catalogue.

### 2. `get_order_status`
- Method: `GET`
- URL: `https://YOUR-SERVICE.onrender.com/orders/{order_id}`
- Parameter: `order_id` (string, required)
- Description: Retrieve the latest status and delivery details for a customer order. Ask the customer for their order reference if they have not provided it.

### 3. `calculate_delivery_fee`
- Method: `GET`
- URL: `https://YOUR-SERVICE.onrender.com/delivery/fee`
- Parameter: `destination` (string, required)
- Description: Calculate the delivery fee and estimated delivery time for a destination. Use the customer's stated town or delivery area.

No credentials are required for this fictional test API. Do not put real customer data or secrets in this mock service.
