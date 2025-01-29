# Receipt Processor

This project provides a web service for processing receipts and calculating points based on predefined rules.

---

## Getting Started

Follow the steps below to get the application up and running.

### Prerequisites

Make sure you have **Docker** installed.

---

## Steps to Run the Application

1. **Clone the Repository**

   ```
   git clone https://github.com/cotraak/fetch-receipt-processor.git
   cd fetch-receipt-processor
   ```

2. **Build the Docker Image**

   `docker build -t receipt-processor-python .`

3. **Run the container and expose it on port 8080**

   `docker run -p 8080:8080 receipt-processor-python`

The application will be running at: http://localhost:8080

4. **Test the application**

   Process Receipt:

   ```
   curl -X POST http://localhost:8080/receipts/process -H "Content-Type: application/json" -d '{
   "retailer": "Target",
   "purchaseDate": "2022-01-01",
   "purchaseTime": "13:01",
   "items": [{"shortDescription": "Mountain Dew 12PK", "price": "6.49"}],
   "total": "6.49"
   }'
   ```

   Get Points:
   ```
   curl http://localhost:8080/receipts/{id}/points
   ```
