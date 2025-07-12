from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import bcrypt
from werkzeug.utils import secure_filename
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            flash("Login successful!")
            return redirect(url_for('user_dashboard', user_id=user['id']))  # ✅ FIXED HERE
        else:
            flash("Invalid credentials. Try again.")

    return render_template('login.html')


# ---------- Dashboard ----------
@app.route('/user_dashboard/<int:user_id>')
def user_dashboard(user_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()

    cur.execute("SELECT * FROM items WHERE user_id = %s", (user_id,))
    items = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('user_dashboard.html', user=user, items=items)


# ---------- Add Item ----------
@app.route('/add_item/<int:user_id>', methods=['POST'])
def add_item(user_id):
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    image = request.files['image']

    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO items (user_id, name, description, image_filename, category)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, name, description, filename, category))
        conn.commit()
        cur.close()
        conn.close()

    return redirect(url_for('user_dashboard', user_id=user_id))


# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
