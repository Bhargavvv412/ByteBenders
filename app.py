from flask import Flask, render_template, request, redirect, url_for, flash
import bcrypt
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------- Home ----------
@app.route('/')
def home():
    return render_template('base.html')

# ---------- Sign Up ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already exists. Try logging in.")
            cursor.close()
            conn.close()
            return redirect(url_for('login'))

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, hashed_pw))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Account created successfully. Please log in.")
        return redirect(url_for('login'))

    return render_template('signup.html')

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Try again.")

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
