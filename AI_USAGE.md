# Uso de Inteligencia Artificial en el HackaFESC 2026

## Uso 1
- Herramienta: Gemini
- Para qué se usó: Diagnosticar el error `503 Service Unavailable` al consultar la API de afiliados.
- Prompt principal (resumido): "El comando curl -i http://localhost:8081/afiliados/1098765432 arroja HTTP/1.0 503 Service Unavailable y base de datos no disponible".
- Qué produjo: Me sugirió que la API estaba intentando conectarse a la base de datos usando variables de entorno que no coincidían con el archivo .env, o que la base de datos no había terminado su script de carga.
- Qué modificó o corrigió el equipo: Rediseñamos el archivo de la API (app.py) para que leyera directamente los archivos CSV locales y de esta manera evitamos por completo el bloqueo de red de la base de datos Postgres.

## Uso 2
- Herramienta: Gemini
- Para qué se usó: Detectar la razón por la cual la base de datos postgres no inicializaba correctamente.
- Prompt principal (resumido): "docker compose logs cierre-db arroja timeout y dice Skipping initialization".
- Qué produjo: Analizó los logs y explicó que la base de datos nunca corrió el script de inicialización `02_load.sql` y que, por lo tanto, no se completaba la inyección de los archivos CSV. 
- Qué modificó o corrigió el equipo: Reconstruimos la infraestructura mediante comandos `docker compose down -v` y `docker compose up -d` para asegurar que los volúmenes corruptos fueran completamente eliminados y que se crearan volúmenes limpios desde cero.

## Uso 3
- Herramienta: Gemini
- Para qué se usó: Desarrollar el archivo procesar.py para generar el output con los archivos esperados.
- Prompt principal (resumido): "La prueba T07, T08 y T09 no están coincidiendo, te paso la cabecera de los archivos de entrada para procesar los afiliados".
- Qué produjo: Creó un script en Python capaz de iterar y sanear el formato de fechas, detectar duplicados y filtrar empresas, generando un archivo `totales.txt` y `excepciones.csv` basado en el análisis de los archivos de entrada CSV.
- Qué modificó o corrigió el equipo: Aplicamos el script de Python directamente en el entorno de producción reemplazando el archivo bash defectuoso original, lo cual nos garantizó la recuperación total de los archivos del cierre de afiliados y superó los tests del validador de manera exitosa.