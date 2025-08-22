from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Route to show payment form
@app.route('/')
def payment_form():
    return render_template("payment.html")  # put your HTML in templates/payment.html

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_payment():
    name = request.form['name']
    gender = request.form['gender']
    address = request.form['address']
    email = request.form['email']
    pincode = request.form['pincode']
    card_type = request.form['card_type']
    expiration = request.form['date']
    cvv = request.form['cvv']
    card_number = request.form['card_number']
    amount = request.form['amount']   # NEW

    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO payments (name, gender, address, email, pincode, card_type, expiration, cvv, card_number, amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, gender, address, email, pincode, card_type, expiration, cvv, card_number, amount))
    conn.commit()
    conn.close()

    return f"<h2>Payment Successful!</h2><p>Thank you {name}, your payment of ₹{amount} has been recorded.</p>"

# Helper to fetch all payments
def get_all_payments():
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Route to display all records
@app.route('/records')
def view_records():
    rows = get_all_payments()

    html = """
    <html>
    <head>
        <title>Payment Records</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; }
            h2 { color: #333; }
            table { border-collapse: collapse; width: 100%; background: white; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
            th { background: #333; color: white; }
            tr:nth-child(even) { background: #f9f9f9; }
        </style>
    </head>
    <body>
        <h2>All Payment Records</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Gender</th>
                <th>Address</th>
                <th>Email</th>
                <th>Pincode</th>
                <th>Card Type</th>
                <th>Expiration</th>
                <th>CVV</th>
                <th>Card Number</th>
                <th>Amount</th>
            </tr>
    """

    for row in rows:
        html += "<tr>"
        for col in row:
            html += f"<td>{col}</td>"
        html += "</tr>"

    html += """
        </table>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    app.run(debug=True)
