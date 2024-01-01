python3 manage.py migrate &&
  uwsgi --socket :8000 --wsgi-file ahmadiwoodwork/wsgi.py
