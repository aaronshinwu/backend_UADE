🎹 Brenda Wu Website

Bienvenido al sitio web de Brenda Wu, pianista 🎼. Este proyecto permite a los visitantes:

Navegar por el sitio fácilmente 🖱️

Enviar mensajes a través de un formulario de contacto 💌

Gestionar los mensajes desde un portal de administración 🔒 (solo accesible para administradores)



⚙️ Tecnologías utilizadas

Frontend: React + Vite ⚛️

Backend: Django 🐍

Base de datos: MySQL 🗄️

Contenedores: Docker 🐳



🚀 Instalación y configuración


Backend (Django + MySQL con Docker)

Construir y levantar el contenedor del backend:

docker-compose up --build

Crear el superusuario de Django dentro del contenedor:

docker-compose run --rm api python manage.py createsuperuser


Frontend (React + Vite)

Ir a la carpeta Frontend

Instalar dependencias:

npm install

Correr el frontend:

npm run dev