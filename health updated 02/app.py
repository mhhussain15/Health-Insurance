from flask import Flask, render_template, request, redirect, url_for, session
import random
import time  # <--- important!

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dummy users
users = {'user1': 'password1', 'user2': 'password2'}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_message="Invalid credentials, please try again.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    time.sleep(5)  # <-- This simulates the processing delay

    if 'submit_manual' in request.form:
        attributes = request.form.to_dict()
        print(attributes)
        predicted_cost = round(random.uniform(3000, 5000), 2)
        return render_template('index.html', predicted_cost=predicted_cost, message="Prediction Successful!")

    if 'submit_prescription' in request.form:
        if 'prescription' not in request.files:
            return render_template('index.html', error_message="No file uploaded!")

        prescription_file = request.files['prescription']
        if prescription_file.filename == '':
            return render_template('index.html', error_message="No selected file!")

        predicted_cost = round(random.uniform(3000, 5000), 2)
        return render_template('index.html', predicted_cost=predicted_cost, message="Prescription Analyzed!")

    return render_template('index.html', error_message="Invalid request!")

if __name__ == '__main__':
    app.run(debug=True)
