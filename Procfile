release: python manage.py migrate
web: daphne mysite.asgi:application --port $PORT
web2: gunicorn mysite.wsgi