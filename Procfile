
heroku config:set DJANGO_SETTINGS_MODULE=Microsoft_Teams.settings --account teams121
web: daphne Microsoft_Teams.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2
heroku ps:scale worker=1:free -a teams121