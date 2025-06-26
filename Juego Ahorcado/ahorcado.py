import psycopg2
import random

# 🔌 Conexión a PostgreSQL
def obtener_conexion():
    return psycopg2.connect(
        dbname="ahorcado",
        user="postgres",
        password="Admin18",
        host="localhost",
        port=5432
    )

# ⚙ Inicializar tablas y palabras
def inicializar_base_datos():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS palabras (
            id SERIAL PRIMARY KEY,
            palabra TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id SERIAL PRIMARY KEY,
            palabra TEXT NOT NULL,
            resultado TEXT,
            intentos_restantes INTEGER
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM palabras")
    if cursor.fetchone()[0] == 0:
        palabras = ["perro", "marciano", "programación", "código", "gato"]
        cursor.executemany(
            "INSERT INTO palabras (palabra) VALUES (%s)",
            [(palabra,) for palabra in palabras]
        )

    conn.commit()
    conn.close()