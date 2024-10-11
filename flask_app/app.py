from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import csv

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


def search_csv_for_id(unique_id):
    file_path = '/home/mgtm98/mahmoud/flask_app/data.csv'  # Path to your CSV file

    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['unique_id'] == unique_id:
                return row['name'], row['department'], row['payment_state']
    
    return None  # Return None if not found

@app.route('/qr-data', methods=['POST'])
def qr_data():
    qr_content = request.json.get('qr_content', '')

    if qr_content:
        data = search_csv_for_id(qr_content)
        if data:
            # Prepare the redirect URL with the retrieved data
            name, department, payment_state = data
            return jsonify({
                'status': 'success',
                'redirect_url': url_for('display', name=name, department=department, payment_state=payment_state)
            })
        else:
            return jsonify({'status': 'error', 'message': 'ID not found in database'})
    
    return jsonify({'status': 'error', 'message': 'No content received'})

@app.route('/display')
def display():
    name = request.args.get('name')
    department = request.args.get('department')
    payment_state = request.args.get('payment_state')
    return render_template('display.html', name=name, department=department, payment_state=payment_state)

if __name__ == '__main__':
    app.run(debug=True)
