# 📊 Cloud System Monitor

Sistema de monitoreo de recursos en tiempo real desplegado en AWS, utilizando Docker para la orquestación de servicios y Grafana para la visualización.

![Dashboard] <img width="1620" height="703" alt="dashboard" src="https://github.com/user-attachments/assets/99e2437a-0238-4377-8817-3290f3ed9ae0" />

## 🚀 Tecnologías
- **Cloud:** AWS EC2 (Ubuntu 24.04).
- **Containerization:** Docker & Docker Compose.
- **Backend:** Python 3 (Psutil, Scikit-learn para predicciones).
- **Database:** PostgreSQL.
- **Visualization:** Grafana.

## ⚙️ Arquitectura
1. **Python Agent:** Recolecta métricas del sistema cada segundo y calcula predicciones de agotamiento de RAM.
2. **PostgreSQL:** Almacena el histórico de métricas.
3. **Grafana:** Lee de la DB y muestra gráficos en tiempo real.

## 🔧 Instalación y Despliegue
Este proyecto está containerizado. Para correrlo:

```bash
1. Clonar el repositorio:
git clone [https://github.com/tiagoferreyra/docker-system-monitor.git](https://github.com/tiagoferreyra/docker-system-monitor.git)
cd docker-system-monitor
2. Crear un archivo llamado .env y agregar:
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=monitordb
3. Levantar los servicios:
docker compose up -d --build

## 🌐 Acceso
Una vez levantado, accede al dashboard desde tu navegador:

- **Si corres en Local:** `http://localhost:3000`
- **Si corres en AWS/Cloud:** `http://<TU_IP_PUBLICA>:3000`

Credenciales por defecto: admin / admin
