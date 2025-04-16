from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import datetime
import os

app = Flask(__name__)

db_file = 'database.db'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sign-in-mobile')
def sign_in_mobile():
    return render_template('sign-in-mobile.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route('/gift_cards')
def gift_cards():
    return render_template('gift_cards.html')

@app.route('/corporate')
def corporate():
    return render_template('corporate_gift_cards.html')

@app.route('/how-to-use')
def how_to_use():
    return render_template('how_to_use.html')

@app.route('/terms-conditions')
def terms_conditions():
    return render_template('terms.html')

@app.route('/luxe')
def luxe():
    return render_template('luxe.html')

@app.route('/getapp')
def get_app():
    return render_template('get_app.html')

@app.route('/makeup-store')
def makeup_store():
    return render_template('makeup.html')

@app.route('/makeup-products')
def makeup_products():
    return render_template('makeup_products.html')


@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json["message"].strip().lower()
    
    bot_reply = responses.get(user_message, "I'm not sure about that, but I'm learning every day!")

    return jsonify({"reply": bot_reply})

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

def generate_otp():
    return str(random.randint(100000, 999999))

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


    print(f"OTP for {mobile_number}: {otp}")

    return jsonify({'message': 'OTP generated and saved successfully'})


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
        
responses = {
    "hello": "Hi there! How can I assist you today?",
    "hii": "Hii there! What's on your mind today?",
    "how are you": "I'm just a chatbot, but I'm doing great!",
    "help": "Sure! You can ask me about products, offers, or anything related to Allora!",
    "what are your offers": "We have amazing discounts on skincare, makeup, and more! Check them out on Allora.",
    "contact support": "You can contact our support team at support@allora.com.",
    "bye": "Goodbye! Have a great day! 😊",
    "best skincare products for oily skin": "For oily skin, we recommend our Oil-Free Moisturizer, Salicylic Acid Cleanser, and Matte Sunscreen. These help control excess oil while keeping your skin hydrated and protected.",
    "skincare for oily skin": "Use Oil-Free Moisturizer, Good Cleanser, and Matte Sunscreen.",
    "recommend a good moisturizer for dry skin": "Try our Hydrating Cream, which is rich in hyaluronic acid and glycerin. It will deeply moisturize and nourish your skin without feeling greasy.",
    "best moisturizer for dry skin": "1. CeraVe Moisturizing Cream 2. Neutrogena Hydro Boost Water Gel",
    "best moisturizer for sensitive skin": "1. Avene Skin Recovery Cream 2. Cetaphil Daily Hydrating Lotion",
    "best sunscreen for sensitive skin": "Our Mineral Sunscreen SPF 50 is perfect for sensitive skin. It’s made with zinc oxide and is free from fragrances and harmful chemicals.",
    "how do i build a daily skincare routine": "Start with a gentle cleanser, followed by a toner to balance your skin, then apply a serum for targeted treatment. Finish with a moisturizer and sunscreen during the day. In the evening, you can add a retinol treatment for nighttime repair.",
    "benefits of vitamin c in skincare": "Vitamin C is a powerful antioxidant that brightens the skin, evens out skin tone, and reduces signs of aging by stimulating collagen production.",
    "can you help me find the perfect foundation shade": "Of course! You can take our foundation shade quiz, which will guide you based on your skin tone, undertone, and preferences. If you need help, feel free to ask our chatbot!",
    "do you have waterproof mascara": "Yes, we have a Waterproof Lash Extension Mascara that will stay put all day, even in humid conditions, without smudging or flaking.",
    "do you offer free shipping": "Yes! We offer free shipping on all orders over Rs.299. For orders under that amount, shipping is just a small flat fee.",
    "how can i track my order": "Once your order is shipped, you’ll receive a tracking number via email or WhatsApp. You can use this number to track your package on our website or through the carrier.",
    "how do i apply a face mask correctly": "Apply an even layer of your favorite face mask to cleansed skin, avoiding the eyes and mouth. Leave it on for the recommended time, then rinse off with warm water. For best results, follow up with a moisturizer.",
    "best setting spray for long-lasting makeup": "Our Long-Lasting Setting Mist keeps your makeup in place for up to 16 hours, providing a matte or dewy finish depending on your preference.",
    "moisturizer for all skin types": "The Ordinary Natural Moisturizing Factors + HA",
    "budget friendly fragrances": "1. Plum BodyLovin' Vanilla Caramello Eau De Parfum 2. Insight Cosmetics Heart Beat Eau De Perfume 3. Moi by Nykaa Joie De Vivre Eau De Parfum 4. Nykaa Wanderlust Fragrance Body Mist - Japanese Cherry Blossom 5. Skinn by Titan Celeste Perfume For Women EDP"
}

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect("database.db") 
    conn.row_factory = sqlite3.Row 
    return conn

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["image"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)


    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO images (filename, filepath) VALUES (?, ?)", 
                   (file.filename, file_path))
    conn.commit()
    conn.close()

    return jsonify({"filename": file.filename, "filepath": file_path})

if __name__ == '__main__':
    app.run(debug=True)
