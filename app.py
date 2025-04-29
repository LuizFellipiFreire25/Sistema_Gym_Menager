
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_type'] = user[4]
            session['user_email'] = user[2]

            if user[4] == 'Administrador':
                return redirect(url_for('admin_dashboard'))
            elif user[4] == 'Aluno':
                return redirect(url_for('aluno_dashboard'))
            elif user[4] == 'Personal':
                return redirect(url_for('personal_dashboard'))

        return render_template('login.html', error='Credenciais inválidas')

    return render_template('login.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if session['user_type'] != 'Administrador':
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html')

@app.route('/aluno')
@login_required
def aluno_dashboard():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    return render_template('aluno/dashboard.html')

@app.route('/personal')
@login_required
def personal_dashboard():
    if session['user_type'] != 'Personal':
        return redirect(url_for('login'))
    return render_template('personal/dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
