import psutil
import time
import os
import psycopg2
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

# Configuración de DB desde variables de entorno
DB_HOST = "db"
DB_NAME = os.getenv("POSTGRES_DB", "monitordb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "mi_password_secreto")

# Conexión a la base de datos
while True:
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = conn.cursor()
        print("✅ Conexion a base de datos exitosa")
        break
    except Exception as e:
        print(f"⏳ Esperando a la base de datos... ({e})")
        time.sleep(5)

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS registro_monitor (
    id SERIAL PRIMARY KEY,
    tiempo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_uso FLOAT,
    ram_uso FLOAT,
    disco_uso FLOAT,
    red_enviada FLOAT,
    red_recibida FLOAT
);
""")
conn.commit()

# Modelo de IA simple (Regresión Lineal)
model = LinearRegression()
ram_history = []
time_history = []

def obtener_datos(last_net, last_time):
    # 1. CPU, RAM, Disco
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage('/').percent

    # 2. Red (Velocidad)
    net = psutil.net_io_counters()
    now = time.time()
    
    delta_time = now - last_time
    if delta_time <= 0: delta_time = 1  # Evitar división por cero

    sent_mb = (net.bytes_sent - last_net.bytes_sent) / (1024 * 1024) / delta_time
    recv_mb = (net.bytes_recv - last_net.bytes_recv) / (1024 * 1024) / delta_time

    return cpu, ram, disco, sent_mb, recv_mb, net, now

def predecir_colapso(ram_uso):
    ahora_timestamp = time.time()
    ram_history.append(ram_uso)
    time_history.append(ahora_timestamp)

    # Mantener solo los últimos 60 datos (1 minuto aprox)
    if len(ram_history) > 60:
        ram_history.pop(0)
        time_history.pop(0)

    # Necesitamos al menos 10 datos para predecir algo útil
    if len(ram_history) < 10:
        return

    # Entrenar modelo
    X = np.array(time_history).reshape(-1, 1)
    y = np.array(ram_history)
    model.fit(X, y)

    tendencia = model.coef_[0]
    
    # Si la tendencia es positiva (la RAM sube)
    if tendencia > 0.01: 
        intercepto = model.intercept_
        # 100 = m*x + b  ->  x = (100 - b) / m
        segundos_colapso = (100 - intercepto) / tendencia
        
        try:
            fecha_colapso = datetime.datetime.fromtimestamp(segundos_colapso)
            ahora = datetime.datetime.now()
            tiempo_restante = fecha_colapso - ahora
            
            if tiempo_restante.total_seconds() < 0:
                return

            minutos = tiempo_restante.seconds // 60
            horas = minutos // 60
            
            if tiempo_restante.days > 30:
                print("✅ Tendencia de subida muy lenta (Seguro a largo plazo).")
            else:
                mensaje = f"🤖 IA: La RAM se agotará en {tiempo_restante.days} días, {horas} hs y {minutos%60} min."
                print(mensaje)

        except Exception as e:
            print(f"Error calculando fecha: {e}")

def main():
    last_net = psutil.net_io_counters()
    last_time = time.time()
    ciclos = 0

    print("🚀 Sistema de Telemetría Avanzada Iniciado con Funciones de IA...")

    while True:
        # Obtener datos
        info_cpu, info_ram, info_disco, mb_sent, mb_recv, last_net, last_time = obtener_datos(last_net, last_time)

        # Analizar con IA
        predecir_colapso(info_ram)

        # Guardar en DB
        try:
            cursor.execute(
                "INSERT INTO registro_monitor (cpu_uso, ram_uso, disco_uso, red_enviada, red_recibida) VALUES (%s, %s, %s, %s, %s)",
                (info_cpu, info_ram, info_disco, mb_sent, mb_recv)
            )
            conn.commit()

            # Log
            print(f"📊 CPU:{info_cpu}% | RAM:{info_ram}% | DISCO:{info_disco}% | ⬇️ {mb_recv:.2f} MB/s | ⬆️ {mb_sent:.2f} MB/s")

        except Exception as e:
            print(f"❌ Error DB: {e}")
            conn.rollback()
        
        # Esperar 1 segundo
        time.sleep(1)
        ciclos += 1

if __name__ == "__main__":
    main()