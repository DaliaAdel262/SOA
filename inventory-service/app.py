from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

# Connect to SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=EcommerceSystem;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# ----------------------------
# Check stock availability
# ----------------------------
@app.route("/api/inventory/check/<int:product_id>", methods=["GET"])
def check_stock(product_id):
    cursor.execute("SELECT ProductID, ProductName, QuantityAvailable, UnitPrice FROM Inventory WHERE ProductID = ?", (product_id,))
    row = cursor.fetchone()
    if row:
        return jsonify({
            "product_id": row.ProductID,
            "product_name": row.ProductName,
            "quantity_available": row.QuantityAvailable,
            "unit_price": float(row.UnitPrice)
        })
    return jsonify({"error": "Product not found"}), 404

# ----------------------------
# Update inventory after an order
# ----------------------------
@app.route("/api/inventory/update", methods=["PUT"])
def update_stock():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity_sold = data.get('quantity_sold')  # must match JSON key from Postman

    if product_id is None or quantity_sold is None:
        return jsonify({"error": "Missing product_id or quantity_sold"}), 400

    # Get current stock
    cursor.execute("SELECT QuantityAvailable FROM Inventory WHERE ProductID = ?", (product_id,))
    row = cursor.fetchone()
    if row is None:
        return jsonify({"error": "Product not found"}), 404

    new_quantity = row.QuantityAvailable - quantity_sold
    if new_quantity < 0:
        return jsonify({"error": "Not enough stock"}), 400

    # Update inventory in database
    cursor.execute("UPDATE Inventory SET QuantityAvailable = ? WHERE ProductID = ?", (new_quantity, product_id))
    conn.commit()

    return jsonify({
        "message": "Inventory updated successfully",
        "product_id": product_id,
        "new_quantity": new_quantity
    })

# ----------------------------
# Run Flask app
# ----------------------------
if __name__ == "__main__":
    app.run(port=5002)
