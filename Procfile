[build]
builder = "heroku/buildpacks:20"

[start]
cmd = "gunicorn karosgym.wsgi:application --bind 0.0.0.0:$PORT --log-file -"
  # Railway asigna dinámicamente el puerto en la variable $PORT

