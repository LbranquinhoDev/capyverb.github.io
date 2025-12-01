#!/bin/bash
echo "🚀 Iniciando build no Railway..."


pip install -r requirements.txt

mkdir -p static/css
mkdir -p static/js  
mkdir -p static/images
mkdir -p staticfiles


echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Aplicando migrações..."
python manage.py migrate

echo "Build feito"