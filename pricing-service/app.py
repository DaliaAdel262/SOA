from flask import Flask, request, jsonify
import requests
import pyodbc

app = Flask(__name__)

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=EcommerceSystem;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

@app.route("/api/pricing/calculate", methods=["POST"])
def calculate_price():
    data = request.get_json()
    final_products = []
    total = 0

    for item in data['products']:
        product_id = item['product_id']
        quantity = item['quantity']

        # Get price from Inventory Service
        response = requests.get(f"http://localhost:5002/api/inventory/check/{product_id}")
        if response.status_code != 200:
            return jsonify({"error": f"Product {product_id} not found"}), 404
        product = response.json()
        unit_price = product['unit_price']

        # Check discount rules
        cursor.execute("SELECT DiscountPercentage FROM PricingRules WHERE ProductID = ? AND MinQuantity <= ?", (product_id, quantity))
        row = cursor.fetchone()
        discount = row.DiscountPercentage if row else 0

        final_price = unit_price * quantity * (1 - discount / 100)
        final_products.append({
            "product_id": product_id,
            "unit_price": unit_price,
            "quantity": quantity,
            "discount": discount,
            "final_price": final_price
        })
        total += final_price

    return jsonify({"products": final_products, "total": total})

if __name__ == "__main__":
    app.run(port=5003)
