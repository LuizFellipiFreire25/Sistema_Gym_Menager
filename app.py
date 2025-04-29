
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
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

@app.route('/admin/cadastrar-usuario', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    if session['user_type'] != 'Administrador':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']
        plano = request.form['plano']
        
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, email, senha, tipo, plano) VALUES (?,?,?,?,?)',
                      (nome, email, senha, tipo, plano))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/cadastrar_usuario.html')

@app.route('/admin/ver-usuario', methods=['GET', 'POST'])
@login_required
def ver_usuario():
    if session['user_type'] != 'Administrador':
        return redirect(url_for('login'))
    
    usuario = None
    if request.method == 'POST':
        nome = request.form['nome']
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome,))
        usuario = cursor.fetchone()
        conn.close()
        
    return render_template('admin/ver_usuario.html', usuario=usuario)

@app.route('/admin/cadastrar-plano', methods=['GET', 'POST'])
@login_required
def cadastrar_plano():
    if session['user_type'] != 'Administrador':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        duracao = request.form['duracao']
        valor = request.form['valor']
        beneficios = request.form['beneficios']
        
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO planos (nome, duracao, valor, beneficios) VALUES (?,?,?,?)',
                      (nome, duracao, valor, beneficios))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/cadastrar_plano.html')

@app.route('/admin/registrar-pagamento', methods=['GET', 'POST'])
@login_required
def registrar_pagamento():
    if session['user_type'] != 'Administrador':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND tipo = 'Aluno'", (email,))
        aluno = cursor.fetchone()
        
        if aluno:
            data_pagamento = datetime.now().strftime('%d/%m/%Y')
            mes_referencia = datetime.now().strftime('%m/%Y')
            cursor.execute("INSERT INTO faturas (usuario_id, mes_referencia, data_pagamento, status, nome) VALUES (?, ?, ?, 'Pago', ?)",
                         (aluno[0], mes_referencia, data_pagamento, aluno[1]))
            conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/registrar_pagamento.html')

@app.route('/admin/registrar-presenca', methods=['GET', 'POST'])
@login_required
def registrar_presenca():
    if session['user_type'] != 'Administrador':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND tipo = 'Aluno'", (email,))
        aluno = cursor.fetchone()
        
        if aluno:
            dia_atual = datetime.now().strftime('%A')
            cursor.execute("INSERT INTO presencas (usuario_id, nome, data, status) VALUES (?, ?, ?, 'Presente')",
                         (aluno[0], aluno[1], dia_atual))
            conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/registrar_presenca.html')

@app.route('/admin/relatorio-frequencia')
@login_required
def relatorio_frequencia():
    if session['user_type'] != 'Administrador':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    cursor.execute("SELECT usuario_id, nome, COUNT(*) as total_presencas FROM presencas GROUP BY usuario_id")
    frequencias = cursor.fetchall()
    conn.close()
    
    return render_template('admin/relatorio_frequencia.html', frequencias=frequencias)

@app.route('/admin/status-pagamentos')
@login_required
def status_pagamentos():
    if session['user_type'] != 'Administrador':
        return redirect(url_for('login'))
    
    mes_atual = datetime.now().strftime("%m/%Y")
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome, data_pagamento FROM faturas WHERE mes_referencia = ?", (mes_atual,))
    pagos = cursor.fetchall()
    
    cursor.execute("""
        SELECT nome, email FROM usuarios 
        WHERE tipo = 'Aluno' 
        AND id NOT IN (SELECT usuario_id FROM faturas WHERE mes_referencia = ?)
    """, (mes_atual,))
    nao_pagos = cursor.fetchall()
    
    conn.close()
    return render_template('admin/status_pagamentos.html', pagos=pagos, nao_pagos=nao_pagos)

@app.route('/aluno')
@login_required
def aluno_dashboard():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    return render_template('aluno/dashboard.html')

@app.route('/aluno/treinos')
@login_required
def aluno_treinos():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    email = session['user_email']
    
    cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
    usuario_id = cursor.fetchone()[0]
    
    cursor.execute(
        'SELECT treino FROM treinos_personalizados WHERE aluno_id = ? ORDER BY data_atribuicao DESC LIMIT 1', 
        (usuario_id,)
    )
    treino = cursor.fetchone()
    conn.close()
    
    return jsonify({'treino': treino[0] if treino else None})

@app.route('/aluno/avaliacao', methods=['GET', 'POST'])
@login_required
def aluno_avaliacao():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()
        email = session['user_email']
        
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        aluno_id = cursor.fetchone()[0]
        
        dias_disponiveis = request.form.get('dias_disponiveis')
        horarios_disponiveis = request.form.get('horarios_disponiveis')
        
        cursor.execute("""
            INSERT INTO avaliacoes (aluno_id, disponibilidade, horario, status, personal_id)
            VALUES (?, ?, ?, ?, NULL)
        """, (aluno_id, dias_disponiveis, horarios_disponiveis, "Pendente"))
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Avaliação agendada com sucesso'})
        
    return jsonify({'message': 'Use POST para agendar avaliação'})

@app.route('/aluno/status-avaliacao')
@login_required
def aluno_status_avaliacao():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    email = session['user_email']
    
    cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
    usuario_id = cursor.fetchone()[0]
    
    cursor.execute(
        "SELECT status FROM avaliacoes WHERE aluno_id = ? ORDER BY id DESC LIMIT 1", 
        (usuario_id,)
    )
    status = cursor.fetchone()
    conn.close()
    
    return jsonify({'status': status[0] if status else None})

@app.route('/aluno/progresso', methods=['GET', 'POST'])
@login_required
def aluno_progresso():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    email = session['user_email']
    
    if request.method == 'POST':
        peso = float(request.form.get('peso'))
        altura = float(request.form.get('altura'))
        imc = round(peso / (altura ** 2), 2)
        data_atual = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        aluno_id = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO progresso (aluno_id, data, peso, altura, imc) VALUES (?, ?, ?, ?, ?)",
            (aluno_id, data_atual, peso, altura, imc)
        )
        conn.commit()
        
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    aluno_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT data, peso, altura, imc FROM progresso WHERE aluno_id = ?", (aluno_id,))
    progresso = cursor.fetchall()
    conn.close()
    
    return jsonify({'progresso': progresso})

@app.route('/aluno/fatura')
@login_required
def aluno_fatura():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    email = session['user_email']
    
    cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
    usuario_id = cursor.fetchone()[0]
    
    mes_atual = datetime.now().strftime("%m/%Y")
    cursor.execute(
        'SELECT status FROM faturas WHERE usuario_id = ? AND mes_referencia = ?', 
        (usuario_id, mes_atual)
    )
    status = cursor.fetchone()
    conn.close()
    
    return jsonify({'status': status[0] if status else 'Não encontrada'})

@app.route('/aluno/duvida', methods=['POST'])
@login_required
def aluno_duvida():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    email = session['user_email']
    
    cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
    usuario_id = cursor.fetchone()[0]
    
    cursor.execute(
        "SELECT status FROM duvidas WHERE aluno_id = ? ORDER BY id DESC LIMIT 1", 
        (usuario_id,)
    )
    pendente = cursor.fetchone()
    
    if pendente and pendente[0] == 'Pendente':
        conn.close()
        return jsonify({'error': 'Você já tem uma dúvida pendente'})
    
    duvida = request.form.get('duvida')
    data_atual = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute(
        "INSERT INTO duvidas (aluno_id, data, duvida, resposta, status) VALUES (?, ?, ?, ?, ?)",
        (usuario_id, data_atual, duvida, "Aguardando resposta do personal", "Pendente")
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Dúvida enviada com sucesso'})

@app.route('/aluno/redefinir-senha', methods=['POST'])
@login_required
def aluno_redefinir_senha():
    if session['user_type'] != 'Aluno':
        return redirect(url_for('login'))
    
    email = session['user_email']
    nova_senha = request.form.get('nova_senha')
    
    conn = sqlite3.connect('academia.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET senha = ? WHERE email = ?", (nova_senha, email))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Senha alterada com sucesso'})

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
