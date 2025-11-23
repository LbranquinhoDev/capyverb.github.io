set -e

echo "Instalando dependencias"
pip install -r requirements.txt

echo "Aplicando migrações do banco de dados"
python manage.py collectstatic --noinput

echo "Concluido com sucesso"