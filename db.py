import sqlite3

def update_db():
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()

    # Add 'amount' column if it doesn't exist
    cursor.execute("PRAGMA table_info(payments)")
    columns = [col[1] for col in cursor.fetchall()]

    if "amount" not in columns:
        cursor.execute("ALTER TABLE payments ADD COLUMN amount REAL")
        print("Column 'amount' added successfully!")
    else:
        print("Column 'amount' already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
