web: daphne Microsoft_Teams.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=Microsoft_Teams.settings -v2