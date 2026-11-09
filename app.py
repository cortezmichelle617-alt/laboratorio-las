from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Laboratorio de Ciberseguridad - <a href='/login'>Login</a> | <a href='/registro'>Registro</a>"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        correo = request.form["correo"]
        password = request.form["password"]
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)", (usuario, correo, password))
        conexion.commit()
        conexion.close()
        return "Usuario registrado"
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND password = ?", (usuario, password))
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            return f"Bienvenido {usuario}!"
        else:
            return "Credenciales incorrectas"
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)