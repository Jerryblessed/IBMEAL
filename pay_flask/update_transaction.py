import requests
import sqlite3
import time

LOCAL_DB = "database.sqlite"  # Path to your local database
REMOTE_API = "http://127.0.0.1:5000/transactions"

def fetch_transactions():
    """Fetch transactions from the remote API."""
    try:
        response = requests.get(REMOTE_API)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transactions: {e}")
        return []

def update_local_transactions(transactions):
    """Update the local database with new transactions."""
    conn = sqlite3.connect(LOCAL_DB)
    cursor = conn.cursor()

    for tx in transactions:
        cursor.execute("""
            INSERT INTO transactions (transaction_id, user_id, value, refunded, notes, provider,
                                      telegram_charge_id, provider_charge_id, payment_name, 
                                      payment_phone, payment_email, order_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(transaction_id) DO UPDATE SET
                user_id = excluded.user_id,
                value = excluded.value,
                refunded = excluded.refunded,
                notes = excluded.notes,
                provider = excluded.provider,
                telegram_charge_id = excluded.telegram_charge_id,
                provider_charge_id = excluded.provider_charge_id,
                payment_name = excluded.payment_name,
                payment_phone = excluded.payment_phone,
                payment_email = excluded.payment_email,
                order_id = excluded.order_id
        """, (tx["transaction_id"], tx["user_id"], tx["value"], tx["refunded"], tx["notes"], 
              tx["provider"], tx["telegram_charge_id"], tx["provider_charge_id"], tx["payment_name"], 
              tx["payment_phone"], tx["payment_email"], tx["order_id"]))
    
    conn.commit()
    conn.close()
    print("Local transactions updated successfully.")

if __name__ == "__main__":
    while True:
        transactions = fetch_transactions()
        if transactions:
            update_local_transactions(transactions)
        time.sleep(30)  # Sync every 30 seconds (adjust as needed)
