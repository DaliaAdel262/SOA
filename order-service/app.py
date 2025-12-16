from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
orders = {}
next_order_id = 1

@app.route("/api/orders/create", methods=["POST"])
def create_order():
    global next_order_id
    data = request.get_json()
    try:
        customer_id = data['customer_id']
        products = data['products']
        total_amount = data['total_amount']
    except KeyError:
        return jsonify({"error": "Missing fields"}), 400

    order_id = next_order_id
    next_order_id += 1
    order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "products": products,
        "total_amount": total_amount,
        "timestamp": str(datetime.now())
    }
    orders[order_id] = order
    return jsonify({"order_id": order_id, "status": "confirmed", "timestamp": order["timestamp"]})

@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    if order_id in orders:
        return jsonify(orders[order_id])
    return jsonify({"error": "Order not found"}), 404

if __name__ == "__main__":
    app.run(port=5001)
