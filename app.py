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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Admin check
        if email == 'admin@gmail.com' and password == 'admin':
            session['admin'] = True
            flash("Welcome, Admin!")
            return redirect(url_for('admin_panel'))

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
            return redirect(url_for('user_dashboard', user_id=user['id']))
        else:
            flash("Invalid credentials. Try again.")

    return render_template('login.html')



@app.route('/admin_panel')
def admin_panel():
    if session.get('email') != 'admin@gmail.com':
        flash('Access denied!')
        return redirect(url_for('login'))

    page = request.args.get('page', default=1, type=int)
    per_page = 6
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Get total count
    cur.execute("SELECT COUNT(*) AS total FROM items")
    total_items = cur.fetchone()['total']
    total_pages = (total_items + per_page - 1) // per_page

    # Get paginated items with user emails
    cur.execute("""
        SELECT items.*, users.email
        FROM items
        JOIN users ON items.user_id = users.id
        ORDER BY items.id DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    items = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('admin_panel.html', items=items, page=page, total_pages=total_pages)



@app.route('/approve_item/<int:item_id>')
def approve_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE items SET approved = 1 WHERE id = %s", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Item approved.')
    return redirect(url_for('admin_panel'))

@app.route('/reject_item/<int:item_id>')
def reject_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Item rejected.')
    return redirect(url_for('admin_panel'))


@app.route('/admin/points')
def admin_points():
    if session.get('email') != 'admin@gmail.com':
        flash("Unauthorized access.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, email, points FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('admin_point.html', users=users)

@app.route('/admin/points')
def manage_points():
    if session.get('email') != 'admin@gmail.com':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, email, points FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('admin_point.html', users=users)


@app.route('/admin/points/update/<int:user_id>', methods=['POST'])
def update_points(user_id):
    if session.get('email') != 'admin@gmail.com':
        return redirect(url_for('login'))

    new_points = request.form.get('points')
    try:
        new_points = int(new_points)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET points = %s WHERE id = %s", (new_points, user_id))
        conn.commit()
        cur.close()
        conn.close()
        flash("User points updated successfully.")
    except ValueError:
        flash("Invalid points value.")

    return redirect(url_for('manage_points'))




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
    flash("Logged out successfully.")
    return redirect(url_for('login'))

@app.route('/filter_by_category')
def filter_by_category():
    category = request.args.get('category')

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT items.*, users.email AS poster_email, users.id AS poster_id
        FROM items
        JOIN users ON items.user_id = users.id
        WHERE items.category = %s
    """, (category,))
    items = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('filtered_items.html', items=items, category=category)



@app.route('/request_item/<int:item_id>', methods=['POST'])
def request_item(item_id):
    if 'user_id' not in session:
        flash("Login required.")
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if already requested
    cur.execute("SELECT * FROM requests WHERE item_id=%s AND requester_id=%s", (item_id, user_id))
    existing = cur.fetchone()

    if not existing:
        cur.execute("INSERT INTO requests (item_id, requester_id) VALUES (%s, %s)", (item_id, user_id))
        conn.commit()
        flash("Request sent successfully.")
    else:
        flash("You have already requested this item.")

    cur.close()
    conn.close()

    # ✅ Redirect to dashboard to ensure user and items are loaded properly
    return redirect(url_for('user_dashboard', user_id=user_id))



@app.route('/incoming_requests')
def incoming_requests():
    if 'user_id' not in session:
        flash("Login required.")
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT r.id, r.status, r.request_date, i.name AS item_name, u.name AS requester_name, u.email
        FROM requests r
        JOIN items i ON r.item_id = i.id
        JOIN users u ON r.requester_id = u.id
        WHERE i.user_id = %s
        ORDER BY r.request_date DESC
    """, (user_id,))
    
    requests = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('incoming_requests.html', requests=requests)


@app.route('/update_request/<int:request_id>/<string:action>')
def update_request(request_id, action):
    if action not in ['approve', 'reject']:
        flash("Invalid action.")
        return redirect(url_for('incoming_requests'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE requests SET status = %s WHERE id = %s", (action + 'ed', request_id))
    conn.commit()
    cur.close()
    conn.close()
    flash(f"Request {action}ed successfully.")
    return redirect(url_for('incoming_requests'))


@app.route('/my_requests')
def my_requests():
    if 'user_id' not in session:
        flash("Login required.")
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT r.id, r.status, r.request_date, i.name AS item_name, i.user_id, u.email AS owner_email
        FROM requests r
        JOIN items i ON r.item_id = i.id
        JOIN users u ON i.user_id = u.id
        WHERE r.requester_id = %s
        ORDER BY r.request_date DESC
    """, (user_id,))
    
    requests = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('my_requests.html', requests=requests)



if __name__ == '__main__':
    app.run(debug=True)
