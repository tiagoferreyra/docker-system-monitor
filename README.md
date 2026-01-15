# 🚀 Monitor de Sistema Contenerizado (Full Stack Data Pipeline)

Este proyecto implementa una arquitectura de microservicios para monitorear el rendimiento de un servidor (CPU y RAM) en tiempo real, almacenando los datos históricamente y visualizándolos en un tablero interactivo.

![Arquitectura](https://img.shields.io/badge/Architecture-Microservices-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Latest-F46800?logo=grafana&logoColor=white)

## 📋 Arquitectura del Proyecto

El sistema consta de 3 contenedores orquestados:

1.  **Monitor Service (Python):** Script ETL que utiliza `psutil` para extraer métricas del host y cargarlas en la base de datos.
2.  **Database (PostgreSQL):** Almacenamiento persistente de series temporales.
3.  **Visualization (Grafana):** Tablero de observabilidad conectado a la BD para análisis en tiempo real.

## 🔧 Tecnologías

* **Lenguaje:** Python 3.9
* **Base de Datos:** PostgreSQL 15
* **Infraestructura:** Docker & Docker Compose
* **Librerías:** `psutil`, `psycopg2`
* **Visualización:** Grafana

## 🚀 Cómo ejecutarlo

Este proyecto está contenerizado, por lo que funciona en cualquier máquina con Docker instalado.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tiagoferreyra/docker-system-monitor.git
    cd docker-system-monitor
    ```

2.  **Iniciar los servicios:**
    ```bash
    docker compose up -d --build
    ```

3.  **Acceder al Dashboard:**
    * Entra a `http://localhost:3000` en tu navegador.
    * Credenciales por defecto: `admin` / `admin`.

## 📸 Capturas de Pantalla

![alt text](image-1.png)