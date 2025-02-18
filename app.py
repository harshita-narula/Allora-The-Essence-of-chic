from flask import Flask, render_template

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the sign-in-mobile page
@app.route('/sign-in-mobile')  # New route for the sign-in page
def sign_in_mobile():
    return render_template('sign-in-mobile.html')  # Render sign-in-mobile.html

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/luxe')
def luxe():
    return render_template('luxe.html')


if __name__ == '__main__':
    app.run(debug=True)
