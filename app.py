from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite que frontend y backend se comuniquen

# Crear tabla si no existe
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT,
                cantidad INTEGER,
                precio REAL,
                fecha TEXT
            )
        ''')

@app.route("/guardar", methods=["POST"])
def guardar():
    data = request.json  # espera JSON con productos
    with sqlite3.connect("database.db") as conn:
        for item in data["carrito"]:
            conn.execute(
                "INSERT INTO pedidos (producto, cantidad, precio, fecha) VALUES (?, ?, ?, ?)",
                (item["nombre"], item["cantidad"], item["precio"], data["fecha"])
            )
    return jsonify({"status": "ok", "mensaje": "Datos guardados en SQLite"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
