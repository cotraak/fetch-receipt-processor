from flask import Flask, request, jsonify
import uuid
import re
from datetime import datetime

app = Flask(__name__)

receipts = {}

def validate_receipt(receipt):
    if not isinstance(receipt, dict):
        return False

    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    if not all(field in receipt for field in required_fields):
        return False

    if not re.match(r"^[\w\s\-&]+$", receipt["retailer"]):
        return False
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", receipt["purchaseDate"]):
        return False
    if not re.match(r"^\d{2}:\d{2}$", receipt["purchaseTime"]):
        return False
    if not re.match(r"^\d+\.\d{2}$", receipt["total"]):
        return False
    if not isinstance(receipt["items"], list) or len(receipt["items"]) < 1:
        return False

    for item in receipt["items"]:
        if not validate_item(item):
            return False

    return True

def validate_item(item):
    if not isinstance(item, dict):
        return False
    if "shortDescription" not in item or "price" not in item:
        return False
    if not re.match(r"^[\w\s\-]+$", item["shortDescription"].strip()):
        return False
    if not re.match(r"^\d+\.\d{2}$", item["price"]):
        return False
    return True

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    data = request.get_json()
    if not data or not validate_receipt(data):
        return jsonify({"error": "Invalid receipt. Please verify input."}), 400

    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = data

    return jsonify({"id": receipt_id}), 200

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    if not re.match(r"^\S+$", receipt_id):
        return jsonify({"error": "Invalid receipt ID."}), 400

    receipt = receipts.get(receipt_id)
    if not receipt:
        return jsonify({"error": "Receipt not found."}), 404

    points = calculate_points(receipt)
    return jsonify({"points": points}), 200

def calculate_points(receipt):
    points = 0

    points += len(re.findall(r"[a-zA-Z0-9]", receipt.get("retailer", "")))

    total = float(receipt.get("total", "0"))
    if total.is_integer():
        points += 50
    
    if total % 0.25 == 0:
        points += 25

    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    for item in items:
        description = item.get("shortDescription", "").strip()
        price = float(item.get("price", "0"))
        if len(description) % 3 == 0:
            points += round(price * 0.2)

    purchase_date = receipt.get("purchaseDate", "")
    if purchase_date:
        day = int(purchase_date.split("-")[2])
        if day % 2 != 0:
            points += 6

    purchase_time = receipt.get("purchaseTime", "")
    if purchase_time:
        purchase_dt = datetime.strptime(purchase_time, "%H:%M")
        if 14 < purchase_dt.hour < 16 or (purchase_dt.hour == 14 and purchase_dt.minute > 0):
            points += 10

    return points


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
