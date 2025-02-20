from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import datetime

app = Flask(__name__)

db_file = 'database.db'  # Using your existing database

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the sign-in-mobile page
@app.route('/sign-in-mobile')
def sign_in_mobile():
    return render_template('sign-in-mobile.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/luxe')
def luxe():
    return render_template('luxe.html')

# Route to save voice input to the database
@app.route('/save_voice_input', methods=['POST'])
def save_voice_input():
    try:
        data = request.get_json()
        print("Received data:", data)
        search_text = data.get('search_text')

        if search_text:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO voice_search (search_text) VALUES (?)", (search_text,))
            conn.commit()
            conn.close()
            print("Data saved successfully!")
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "No search text received"}), 400

    except Exception as e:
        print("Error saving data:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Route to send OTP
@app.route('/send_otp', methods=['POST'])
def send_otp():
    mobile_number = request.json.get('mobile_number')
    if not mobile_number:
        return jsonify({'error': 'Mobile number is required'}), 400

    otp = generate_otp()
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO otp_verification (mobile_number, otp) 
                          VALUES (?, ?)''', (mobile_number, otp))
        conn.commit()

    # Print OTP to console for manual verification
    print(f"OTP for {mobile_number}: {otp}")

    return jsonify({'message': 'OTP generated and saved successfully'})

# Route to verify OTP
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    mobile_number = request.json.get('mobile_number')
    otp = request.json.get('otp')

    if not mobile_number or not otp:
        return jsonify({'error': 'Mobile number and OTP are required'}), 400

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT otp, created_at FROM otp_verification 
                          WHERE mobile_number = ? ORDER BY created_at DESC LIMIT 1''', (mobile_number,))
        row = cursor.fetchone()

        if row:
            stored_otp, created_at = row
            if stored_otp == otp:
                return jsonify({'message': 'OTP verified successfully'})
            else:
                return jsonify({'error': 'Invalid OTP'}), 400
        else:
            return jsonify({'error': 'No OTP found for this mobile number'}), 404

if __name__ == '__main__':
    app.run(debug=True)
