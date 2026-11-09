from flask import Flask, request, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def log_evento(mensaje):
    with open("eventos.log", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}\n")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['usuario']
        passw = request.form['clave']
        
        # CONEXIÓN SEGURA - CORRECCIÓN
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        
        # ANTES (VULNERABLE): f"SELECT * FROM usuarios WHERE usuario='{user}'"
        # AHORA (SEGURO): Usamos placeholders ?
        try:
            cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND clave=?", (user, passw))
            resultado = cursor.fetchone()
            
            if resultado:
                log_evento(f"Login exitoso - usuario: {user}")
                return "¡Login exitoso! - Sistema seguro"
            else:
                log_evento(f"Intento fallido - usuario: {user}")
                return "Credenciales incorrectas - Ataque bloqueado"
        except Exception as e:
            log_evento(f"Intento de inyeccion bloqueado: {user}")
            return f"Ataque detectado y bloqueado: {e}"
        finally:
            conn.close()
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)