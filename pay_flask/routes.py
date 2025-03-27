from flask import Flask, render_template, request, jsonify
import sqlite3
import requests
import logging

app = Flask(__name__)

PAYSTACK_SECRET_KEY = "sk_test_7e747d8832ca52dad6639c6f2b7042e10c5fb6eb"
DATABASE = "../database.sqlite"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    
    transactions_list = [dict(tx) for tx in transactions]
    return jsonify(transactions_list)

def get_user_by_id(user_id):
    """Retrieve user details by user_id"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, first_name, last_name, username FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return {"user_id": user[0], "first_name": user[1], "last_name": user[2], "username": user[3]} if user else None

def update_credit(user_id, amount):
    """Update user's credit balance in the database"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        amount = float(amount)  # Keep decimals

        cursor.execute("SELECT credit FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            new_credit = user[0] + amount  
            cursor.execute("UPDATE users SET credit = ? WHERE user_id = ?", (new_credit, user_id))
            conn.commit()
            logging.info(f"Updated user {user_id} credit to {new_credit}")
        else:
            logging.warning(f"User {user_id} not found!")

        conn.close()
    except Exception as e:
        logging.error(f"Error updating credit: {e}")


@app.route("/")
def home():
    user_id = request.args.get("user")  # Get user_id from URL param
    user = get_user_by_id(user_id) if user_id else None
    return render_template("index.html", user=user)

@app.route("/search", methods=["POST"])
def search_user():
    data = request.json
    name = data.get("name")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, first_name, last_name, username FROM users WHERE first_name LIKE ? OR last_name LIKE ? OR username LIKE ?", 
                   (f"%{name}%", f"%{name}%", f"%{name}%"))
    users = cursor.fetchall()
    conn.close()

    return jsonify([{"user_id": u[0], "first_name": u[1], "last_name": u[2], "username": u[3]} for u in users])

@app.route("/pay", methods=["POST"])
def pay():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    email = data.get("email")

    if not user_id or not amount or not email:
        return jsonify({"status": "failed", "message": "Missing payment details"}), 400

    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}", "Content-Type": "application/json"}
    paystack_data = {
        "email": email,
        "amount": int(float(amount) * 100),  # Convert NGN to kobo safely
        "currency": "NGN",
        "callback_url": f"http://127.0.0.1:5000/payment_callback?user_id={user_id}&amount={amount}"
    }


    response = requests.post("https://api.paystack.co/transaction/initialize", json=paystack_data, headers=headers)
    res_json = response.json()
    
    if res_json.get("status"):
        return jsonify({"status": "success", "pay_url": res_json["data"]["authorization_url"]})
    
    return jsonify({"status": "failed", "message": "Payment initialization failed"})

@app.route("/payment_callback")
def payment_callback():
    """Handles Paystack payment verification and updates user credit"""
    ref = request.args.get("reference")
    user_id = request.args.get("user_id")
    amount = request.args.get("amount")

    if not ref or not user_id or not amount:
        logging.warning("Invalid callback request - missing parameters")
        return "<script>alert('Invalid payment details.'); window.location.href='/';</script>"

    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
    res_json = response.json()

    logging.debug(f"Paystack response: {res_json}")

    if res_json.get("status") and res_json["data"]["status"] == "success":
        update_credit(user_id, amount)
        return "<script>alert('Payment successful!'); window.location.href='/';</script>"

    return "<script>alert('Payment failed or not verified!'); window.location.href='/';</script>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)




