web: gunicorn Microsoft_Teams.wsgi --log-file -
web2: daphne chat.routing:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2