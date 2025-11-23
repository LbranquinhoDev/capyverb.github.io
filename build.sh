echo "🚀 Iniciando deploy no Railway..."

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

echo "✅ Build concluído!"