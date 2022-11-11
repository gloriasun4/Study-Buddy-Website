release: python manage.py migrate
web: gunicorn mysite.wsgi
web2: daphne mysite.asgi:application --port $PORT --bind 0.0.0.0 -v2