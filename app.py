from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def conectar_bd():
    return sqlite3.connect(DATABASE)

@app.route('/eventosAdministrador')
def index():
    conn = conectar_bd()
    c = conn.cursor()
    c.execute('SELECT * FROM eventos_academicos')
    eventos = c.fetchall()
    conn.close()
    return render_template('index.html', eventos=eventos)

@app.route('/eventos')
def mostrar_eventos():
    conn = conectar_bd()
    c = conn.cursor()
    c.execute('SELECT * FROM eventos_academicos ORDER BY fecha DESC')
    eventos = c.fetchall()
    conn.close()
    return render_template('eventos.html', eventos=eventos)

@app.route('/agregar', methods=['POST'])
def agregar_evento():
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    hora = request.form['hora']
    descripcion = request.form['descripcion']  
    conn = conectar_bd()
    c = conn.cursor()
    c.execute('INSERT INTO eventos_academicos (nombre, fecha, hora, descripcion) VALUES (?, ?, ?, ?)', (nombre, fecha, hora, descripcion)) 
    conn.commit()
    conn.close()
    return redirect('/eventosAdministrador')

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
        descripcion = request.form['descripcion']  
        conn = conectar_bd()
        c = conn.cursor()
        c.execute('UPDATE eventos_academicos SET nombre = ?, fecha = ?, hora = ?, descripcion = ? WHERE id = ?', (nombre, fecha, hora, descripcion, id))  
        conn.commit()
        conn.close()
        return redirect('/eventosAdministrador')

@app.route('/nuevo')
def nuevo_evento():
    return render_template('nuevo.html')
