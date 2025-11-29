#!/bin/sh
# Salir si hay algún error
set -e

echo "Iniciando aplicación FORMULARIO_CONTACTO_API..."

# Migraciones de base de datos
echo "Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate --noinput

# Crear superusuario si no existe (comando custom)
echo "Creando superusuario si no existe..."
python manage.py create_initial_superuser

# Recopilar archivos estáticos (CSS, JS, favicon, etc.)
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Aplicación preparada exitosamente"

# Determinar modo de ejecución
MODE=${1}

if [ "$MODE" = "production" ]; then
    echo "Iniciando Gunicorn en modo PRODUCCIÓN..."
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120
else
    echo "Iniciando runserver en modo DESARROLLO..."
    exec python manage.py runserver 0.0.0.0:8000
fi
