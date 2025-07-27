from flask import Flask, render_template, request, redirect, session, ur>
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'SUPERSECRETKEY'

# --- Handle Railway Deployment Database Location ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join("/tmp", "users.db")
#if not os.path.exists(DB_PATH):
#    original_db = os.path.join(BASE_DIR, "db", "users.db")
 #   os.system(f"cp {original_db} {DB_PATH}")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- User Model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# --- Home Page ---
@app.route('/')
def index():
    return redirect(url_for('login'))

# --- Register ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'User already exists'
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password>
        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

# --- Dashboard ---
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

# --- Admin Page ---
@app.route('/admin')
def admin():
    return render_template('admin.html')

# --- Crypto Page ---
@app.route('/crypto')
def crypto():
    return render_template('crypto.html')

# --- Upload Page ---
@app.route('/upload')
def upload():
    return render_template('upload.html')

# --- Logout ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# --- Run Local ---
if __name__ == '__main__':
    app.run(debug=True)

