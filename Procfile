release: python manage.py migrate
release: python manage.py collectstatic
web: daphne Microsoft_Teams.asgi:application --port $PORT --bind 0.0.0.0 -v2
