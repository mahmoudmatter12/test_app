from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

# Hardcoded credentials
USER_CREDENTIALS = {
    'username': 'admin',
    'password': '123'
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['user'] = username  # Store username in session
            return redirect(url_for('hello'))
        else:
            flash('Invalid credentials, please try again.')

    return render_template('login.html')

@app.route('/hello')
def hello():
    if 'user' in session:  # Check if user is logged in
        return render_template('hello.html', username=session['user'])
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    flash('You have been logged out.')
    return redirect(url_for('login'))

# Route to receive QR code data
@app.route('/qr-data', methods=['POST'])
def qr_data():
    qr_content = request.json.get('qr_content', '')
    if qr_content:
        print(f"QR Code Content: {qr_content}")  # Output to terminal
        return jsonify({'status': 'success', 'message': 'QR content received'})
    return jsonify({'status': 'error', 'message': 'No content received'})

if __name__ == '__main__':
    app.run(debug=True)
