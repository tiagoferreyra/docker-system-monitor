import psutil as pu
import psycopg2
import time
import os

"""
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "mi_password_secreto" 
DB_PORT = "5432"
"""
# Ahora las credenciales leen del entorno, o usan un defecto si no existen
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_DB', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'mi_password_secreto')
DB_PORT = os.getenv('DB_PORT', '5432')

def init_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )

        cur = conn.cursor()

        sql_crear_tabla = """
            CREATE TABLE IF NOT EXISTS registro_monitor(
                id SERIAL PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cpu_uso FLOAT,
                ram_uso FLOAT
            );
        """
        cur.execute(sql_crear_tabla)

        conn.commit()

        cur.close
        conn.close
        print("BD iniciada")
    except Exception as e:
        print(f"Error al conectar: {e}")

def guardar_dato(cpu_val, ram_val):
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
        cur = conn.cursor()

        #huecos %s (psycopg2)
        sql = "INSERT INTO registro_monitor (cpu_uso, ram_uso) VALUES (%s, %s)"
        
        cur.execute(sql, (cpu_val, ram_val))

        conn.commit()
        cur.close()
        conn.close()
        print('guardado')

    except Exception as e:
        print(f"Error guardando dato: {e}")


def ram():
    ram = pu.virtual_memory()

    convert = 1024 ** 3

    info = {
        "Total": round((ram.total / convert),2),
        "Disponible": round((ram.available / convert),2),
        "Usada": round((ram.used / convert),2),
        "Libre": round((ram.free / convert),2),
    }
    return info

def cpu():
    cpu = pu.cpu_percent(interval=1)
    return cpu


def main():
   
    init_db()

    while True:
        info_ram = ram()
        info_cpu = cpu()
        print(f"Uso de CPU: {info_cpu}%, Uso de RAM: {info_ram}")
        guardar_dato(info_cpu, info_ram['Usada'])
        time.sleep(5)

if __name__ == "__main__":
    main()