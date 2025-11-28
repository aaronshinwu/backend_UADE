#!/bin/sh

# Salga si hay error
set -e

echo "Iniciando aplicacion FORMULARIO_CONTACTO_API"

# Estos comandos se ejecutan ahora DENTRO de la carpeta Backend
echo "Ejecutando migraciones de base de datos..."
python manage.py makemigrations
python manage.py migrate --noinput

# ESTA ES LA LÍNEA MODIFICADA: Ahora usa el comando estándar de Django
echo "Creando superusuario (no interactivo)..."
python manage.py createsuperuser --noinput

echo "Recopilando archivos estaticos..."
python manage.py collectstatic --noinput --clear

echo "Aplicacion preparada exitosamente"

MODE=${1}

if [ "$MODE" = "production" ]; then
    echo "Iniciando en modo PRODUCCION con GUNICORN"
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120
else
    echo "Iniciando en modo DESARROLLO con runserver"
    exec python manage.py runserver 0.0.0.0:8000
fi