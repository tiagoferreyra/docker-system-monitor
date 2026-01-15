import psutil
import psycopg2
import time
import os

# --- CONFIGURACIÓN ---
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB', 'postgres')
DB_USER = os.getenv('POSTGRES_USER', 'postgres') 
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'mi_password_secreto')
DB_PORT = os.getenv('DB_PORT', '5432')

# --- CONEXIÓN DB ---
conn = None
while conn is None:
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
        print("✅ Conexion a base de datos exitosa")
    except Exception as e:
        print(f"⏳ La base de datos aun no esta lista ({e}), reintentando en 2s...")
        time.sleep(2)

cursor = conn.cursor()

# --- MIGRACIÓN ---
cursor.execute("DROP TABLE IF EXISTS registro_monitor;")
cursor.execute("""
    CREATE TABLE registro_monitor (
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        cpu_uso FLOAT,
        ram_uso FLOAT,
        disco_uso FLOAT,        
        red_enviada FLOAT,      
        red_recibida FLOAT      
    );
""")
conn.commit()

print("🚀 Sistema de Telemetría Avanzada Iniciado con Funciones...")

# --- FUNCIONES ---

def obtener_datos(last_net), (last_time):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    
    try:
        disco = psutil.disk_usage('/host_disk').percent
    except:
        disco = psutil.disk_usage('/').percent

    curr_net = psutil.net_io_counters()
    curr_time = time.time()
    time_delta = curr_time - last_time_in
    if time_delta == 0: time_delta = 1 

    bytes_sent = curr_net.bytes_sent - last_net_.bytes_sent
    bytes_recv = curr_net.bytes_recv - last_net_.bytes_recv
    mb_sent = (bytes_sent / 1024 / 1024) / time_delta
    mb_recv = (bytes_recv / 1024 / 1024) / time_delta

    return cpu, ram, disco, mb_sent, mb_recv, curr_net, curr_time

def enviar_telegram(mensaje):
    if TG_TOKEN and TG_CHAT_ID:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        try:
            requests.post(url, data={"chat_id": TG_CHAT_ID, "text": mensaje})
        except Exception as e:
            print(f"Error Telegram: {e}")


def predecir_colapso_ram():
    print("IA: Analizando consumo de RAM")
    
    query = "SELECT fecha, ram_uso FROM registro_monitor ORDER BY fecha DESC LIMIT 100"
    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        print(f"Error leyendo DB: {e}")
        return

    if len(df) < 50:
        print("Recolectando datos para la IA...")
        return

    df['segundos'] = df['fecha'].apply(lambda x: x.timestamp())
    
    df = df.sort_values('segundos')

    X = df['segundos'].values.reshape(-1, 1)
    y = df['ram_uso'].values

    model = LinearRegression()
    model.fit(X, y)
    
    tendencia = model.coef_[0]
    
    # Si la tendencia es muy pequeña o negativa, la RAM está estable
    if tendencia <= 0.001: 
        print("RAM estable o liberándose.")
        return

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
            mensaje = f" IA: La RAM se agotará en {tiempo_restante.days} días, {horas} hs y {minutos%60} min."
            print(mensaje)
            
            if tiempo_restante.days == 0 and horas < 1:
                enviar_telegram(f" PELIGRO: {mensaje}")

    except Exception as e:
        print(f"Error calculando fecha: {e}")

def main():
    last_net = psutil.net_io_counters()
    last_time = time.time()

    ciclos = 0
    
    while True:
        
        cpu, ram, disco, mb_sent, mb_recv, last_net, last_time = obtener_datos(last_net, last_time)

        # 2. Guardar en DB
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

        if ciclos >= 12:
            predecir_colapso_ram()
            ciclos = 0
        

        ciclos += 1
        time.sleep(5)

if __name__ == "__main__":
    main()