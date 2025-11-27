from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# def get_db():
    
#     # Need to adjust to allow remote connections so we can all access same database
#     return mysql.connector.connect(
#         host="localhost",
#         user="ecommerce_user",
#         password="secure_password",
#         database="ecommerce_system"
#     )

@app.get("/api/inventory/check/<int:product_id>")
def check_inventory(product_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory WHERE product_id=%s", (product_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5002, debug=True)
