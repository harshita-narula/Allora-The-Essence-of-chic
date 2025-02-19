from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

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

@app.route('/save_voice_input', methods=['POST'])
def save_voice_input():
    try:
        # Get the voice input from the request
        data = request.get_json()
        print("Received data:", data)  # Print received data for debugging
        search_text = data.get('search_text')

        if search_text:
            # Save the voice input to the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO voice_search (search_text) VALUES (?)", (search_text,))
            conn.commit()
            conn.close()
            print("Data saved successfully!")  # Confirm data was saved
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "No search text received"}), 400

    except Exception as e:
        print("Error saving data:", e)  # Print the error for debugging
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
