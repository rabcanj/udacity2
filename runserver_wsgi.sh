gunicorn --bind 'unix:/home/juraj/Desktop/udacity2/somename.sock' wsgi:application --certfile=dev.crt --keyfile=dev.key
 
