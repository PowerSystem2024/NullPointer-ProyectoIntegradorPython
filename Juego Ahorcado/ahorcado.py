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

def obtener_palabra_aleatoria():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT palabra FROM palabras ORDER BY RANDOM() LIMIT 1")
    palabra = cursor.fetchone()[0]
    conn.close()
    return palabra

# 💾 Guardar resultado de la partida
def guardar_resultado(palabra, resultado, intentos_restantes):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historial (palabra, resultado, intentos_restantes)
        VALUES (%s, %s, %s)
    """, (palabra, resultado, intentos_restantes))
    conn.commit()
    conn.close()

# 🎮 Mostrar tablero
def mostrar_tablero(palabra_secreta, letras_adivinadas):
    tablero = ""
    for letra in palabra_secreta:
        if letra in letras_adivinadas:
            tablero += letra
        else:
            tablero += "_"
    print(tablero)

# 🧠 Lógica principal del juego
def jugar_ahorcado():
    inicializar_base_datos()
    palabra_secreta = obtener_palabra_aleatoria()
    letras_adivinadas = []
    intentos_restantes = 6

    while intentos_restantes > 0:
        mostrar_tablero(palabra_secreta, letras_adivinadas)
        letra = input("Introduce una letra: ").lower()

        if letra in letras_adivinadas:
            print("Ya has introducido esa letra. Probá con otra.")
            continue

        if letra in palabra_secreta:
            letras_adivinadas.append(letra)
            if set(letras_adivinadas) >= set(palabra_secreta):
                print(f"¡Felicidades! Adivinaste la palabra: {palabra_secreta}")
                guardar_resultado(palabra_secreta, "Ganada", intentos_restantes)
                break
        else:
            intentos_restantes -= 1
            print(f"Letra incorrecta. Te quedan {intentos_restantes} intentos.")

    if intentos_restantes == 0:
        print(f"Perdiste. La palabra era: {palabra_secreta}")
        guardar_resultado(palabra_secreta, "Perdida", 0)

# 🚀 Ejecutar el juego
jugar_ahorcado()
