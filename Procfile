release: pipenv run upgrade
web: gunicorn wsgi:app --chdir ./src --bind 0.0.0.0:$PORT
