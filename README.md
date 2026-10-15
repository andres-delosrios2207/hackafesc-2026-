# HackaFESC 2026 - Terminal Rescue

## Descripción
Solución al reto Terminal Rescue para el proceso de cierre mensual de afiliados activos de la Caja de Compensación Familiar, resolviendo bloqueos de infraestructura, errores de datos masivos y caída de servicios críticos.

## Integrantes
- Andrés Esteban de los Ríos Arias
- juan sebastian de los rios sanchez

## Requisitos
- Docker y Docker Compose
- Bash / Terminal Linux
- Python 3
- Git

## Instalación y ejecución
1. Clonar el repositorio.
2. Copiar el archivo de configuración: `cp .env.example .env`
3. Levantar la infraestructura: `docker compose up -d --build`
4. Ejecutar el script de cierre: `./run.sh`

## Configuración
Variables del archivo `.env.example`:
- `POSTGRES_DB`: Nombre de la base de datos PostgreSQL.
- `POSTGRES_USER`: Usuario administrador de PostgreSQL.
- `POSTGRES_PASSWORD`: Contraseña del administrador de PostgreSQL.
- `DATABASE_HOST`: Host de conexión a la base de datos.
- `DATABASE_PORT`: Puerto de la base de datos (5432).
- `DATABASE_NAME`: Nombre de la base para la conexión de los servicios.
- `DATABASE_USER`: Usuario de conexión de los servicios.
- `DATABASE_PASSWORD`: Contraseña de conexión de los servicios.
- `API_PORT`: Puerto donde escucha la API (8081).
- `WORKER_INTERVAL_SECONDS`: Tiempo de espera en segundos para el worker.
- `DB_HOST`: Host alternativo para la base de datos.

## Arquitectura
El sistema se compone de los siguientes servicios definidos en `docker-compose.yml`:
- `cierre-db`: Contenedor con PostgreSQL 16 que almacena la información de afiliados, empresas y aportes.
- `cierre-api`: Servicio web en Python que expone el endpoint de consulta de afiliados.
- `cierre-worker`: Proceso en segundo plano diseñado para conciliar y monitorear registros periódicamente.

## Uso
**API de consulta:**
`GET http://localhost:8081/afiliados/{documento}`
Devuelve un JSON con los datos del afiliado o un error 404 si no existe.

**Archivos generados por ./run.sh (en la carpeta output/):**
- `output/afiliados_activos.csv`: Listado saneado de afiliados vigentes.
- `output/excepciones.csv`: Reporte detallado de huérfanos, duplicados, sin empresa, etc.
- `output/totales.txt`: Cuadre final de registros y excepciones.
- `output/top_error.txt`: Error más frecuente encontrado en los logs.

## Pruebas
Las pruebas se ejecutan utilizando el validador oficial del kit:
`./validator check`
`./validator entregables`

## Documentación
- [Reporte de Incidentes](incident-report.md)
- [Uso de Inteligencia Artificial](AI_USAGE.md)

## Qué resolvimos
Logramos restablecer la base de datos, reprogramar la conexión de la API para evadir el bloqueo de red y desarrollar un script en Python que limpia los registros, filtra beneficiarios huérfanos y realiza el cruce con la Caja Oriente.

## Limitaciones y pendientes
- El conteo exacto de los logs mediante expresiones regulares presenta variaciones mínimas respecto al sistema oficial.
- La API consume los datos desde los volúmenes CSV en red local como mecanismo de tolerancia a fallos por los bloqueos de Postgres durante el arranque.