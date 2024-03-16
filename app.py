from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def conectar_bd():
    return sqlite3.connect(DATABASE)

@app.route('/')
def index():
    conn = conectar_bd()
    c = conn.cursor()
    c.execute('SELECT * FROM eventos_academicos')
    eventos = c.fetchall()
    conn.close()
    return render_template('index.html', eventos=eventos)

@app.route('/agregar', methods=['POST'])
def agregar_evento():
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    hora = request.form['hora']
    conn = conectar_bd()
    c = conn.cursor()
    c.execute('INSERT INTO eventos_academicos (nombre, fecha, hora) VALUES (?, ?, ?)', (nombre, fecha, hora))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    if request.method == 'GET':
        conn = conectar_bd()
        c = conn.cursor()
        c.execute('SELECT * FROM eventos_academicos WHERE id = ?', (id,))
        evento = c.fetchone()
        conn.close()
        return render_template('editar.html', evento=evento)
    elif request.method == 'POST':
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        hora = request.form['hora']
        conn = conectar_bd()
        c = conn.cursor()
        c.execute('UPDATE eventos_academicos SET nombre = ?, fecha = ?, hora = ? WHERE id = ?', (nombre, fecha, hora, id))
        conn.commit()
        conn.close()
        return redirect('/')

@app.route('/nuevo')
def nuevo_evento():
    return render_template('nuevo.html')

if __name__ == '__main__':
    app.run(debug=True)
